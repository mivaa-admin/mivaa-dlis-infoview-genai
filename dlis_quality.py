
from collections import Counter

def generate_dlis_quality_report(logical_file):
    report = []

    DEPTH_MNEMONICS = ['TDEP', 'DEPT', 'DEPTH', 'MD', 'TVD']

    # 1. Missing Depth Channel
    has_depth = any(
        any(ch.name.upper() in DEPTH_MNEMONICS for ch in frame.channels)
        for frame in getattr(logical_file, 'frames', [])
    )
    report.append("### Missing Depth Channel")
    report.append("✅ Found depth channel." if has_depth else "❌ Depth channel not found!")

    # 2. Channels Missing Units
    missing_units = [ch.name for ch in getattr(logical_file, 'channels', []) if not ch.units]
    report.append("### Channels with Missing Units")
    report.append(", ".join(missing_units) if missing_units else "✅ All channels have units.")

    # 3. Duplicate Channels
    names = [ch.name for ch in getattr(logical_file, 'channels', [])]
    duplicates = [name for name, count in Counter(names).items() if count > 1]
    report.append("### Duplicate Channel Names")
    report.append(", ".join(duplicates) if duplicates else "✅ No duplicates.")

    # 4. Frames Without Channels
    empty_frames = [frame for frame in getattr(logical_file, 'frames', []) if not frame.channels]
    report.append("### Frames Without Channels")
    report.append(f"{len(empty_frames)} empty frames found." if empty_frames else "✅ All frames have channels.")

    # 5. Total Curve Families Present
    families = {
        "Gamma Ray": ["GR", "SGR", "CGR"],
        "Resistivity": ["ILD", "LLD", "MSFL", "RT", "RLA", "RLL"],
        "Porosity": ["NPHI", "DPHI", "PHIT", "PHIE"],
        "Density": ["RHOB", "DEN", "ZDEN"],
        "Sonic": ["DT", "DTS", "DTP", "DTCO"],
        "Caliper": ["CALI"],
    }

    family_counts = {fam: 0 for fam in families}
    for ch in getattr(logical_file, 'channels', []):
        for fam, tags in families.items():
            if any(ch.name.upper().startswith(tag) for tag in tags):
                family_counts[fam] += 1
                break

    report.append("### Curve Families Count")
    for fam, count in family_counts.items():
        report.append(f"{fam}: {count}")

    return "\n\n".join(report)

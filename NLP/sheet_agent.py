# =============================================
#   GOOGLE SHEET CONNECTED AGENT
#   Reads student data directly from Google Sheets
#   No MySQL needed - works in real time!
# =============================================

import pandas as pd

# --- STEP 1: Your Google Sheet ID ---
# Replace this with YOUR sheet ID (between /d/ and /edit in the URL)
SHEET_ID = "1vpRazpAADb6JELbw2rOI6yEoe_SE2Iks43g6POTmEik"

# --- STEP 2: Build the CSV export link ---
# Google Sheets can be read as CSV directly using this trick!
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

print("=" * 60)
print("   GOOGLE SHEET MONITORING AGENT")
print("   Reading live data from Google Sheets...")
print("=" * 60)

# --- STEP 3: Read the sheet directly into Python ---
try:
    df = pd.read_csv(SHEET_URL)
except Exception as e:
    print(f"❌ Could not read sheet: {e}")
    print("\n💡 Make sure:")
    print("   1. Sheet is shared as 'Anyone with link - Viewer'")
    print("   2. SHEET_ID is correct")
    exit()

print(f"\n✅ Loaded {len(df)} students from Google Sheet\n")

# --- STEP 4: Calculate risk score for each student ---
results = []

for index, row in df.iterrows():
    name      = row['student_name']
    prn       = row['prn_number']
    phone     = row['parent_phone']
    att_pct   = float(row['attendance_pct'])
    marks_pct = float(row['marks_pct'])
    fee_value = str(row['fee_pending']).strip().lower()
if fee_value in ['paid', '0', 'nan', '']:
    fee_pend = 0.0
else:
    fee_pend = float(row['fee_pending'])
    career    = float(row['career_progress'])

    # Calculate score
    score = round((att_pct * 0.40) + (marks_pct * 0.60), 1)

    # Risk level
    if score < 50:
        risk = "HIGH RISK"
        icon = "🔴"
    elif score < 70:
        risk = "MEDIUM RISK"
        icon = "🟡"
    else:
        risk = "LOW RISK"
        icon = "🟢"

    results.append({
        "name": name, "prn": prn, "phone": phone,
        "att": att_pct, "marks": marks_pct,
        "fee_pending": fee_pend, "career": career,
        "score": score, "risk": risk, "icon": icon
    })

# Sort by score - lowest first
results.sort(key=lambda x: x['score'])

# --- STEP 5: Print Report ---
print(f"  {'Student':<20} {'Attend':>7}  {'Marks':>6}  {'Score':>6}  Risk Level")
print("  " + "-" * 55)

for r in results:
    print(f"  {r['icon']} {r['name']:<18} {r['att']:>6}%  {r['marks']:>5}%  "
          f"{r['score']:>5}/100  {r['risk']}")

# --- STEP 6: Summary ---
high   = [r for r in results if r['risk'] == "HIGH RISK"]
medium = [r for r in results if r['risk'] == "MEDIUM RISK"]
low    = [r for r in results if r['risk'] == "LOW RISK"]
fee_due = [r for r in results if r['fee_pending'] > 0]

print()
print("=" * 60)
print("  SUMMARY")
print(f"  Total students   : {len(results)}")
print(f"  🔴 High Risk     : {len(high)}")
print(f"  🟡 Medium Risk   : {len(medium)}")
print(f"  🟢 Low Risk      : {len(low)}")
print(f"  💰 Fee Pending   : {len(fee_due)}")
print("=" * 60)

if high:
    print()
    print("  ⚠️  HIGH RISK students - immediate action needed:")
    for r in high:
        print(f"     → {r['name']} (Score: {r['score']}/100) - Parent: {r['phone']}")

print()
print("✅ This data is LIVE from your Google Sheet.")
print("   Edit the sheet and run this script again to see updates!")

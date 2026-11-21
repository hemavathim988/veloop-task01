import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.utils import get_column_letter
import blueprint_content as B
import profile_data as P
import analyze_supplementary as AS
import generate_supplementary as GS
import clean_data as CD
import facts as FA
F=FA.F
HF=PatternFill('solid',fgColor='1F3864'); BAN=PatternFill('solid',fgColor='C00000')
thin=Side(style='thin',color='BFBFBF')
def sheet(wb,name,headers,rows,banner=None,widths=None):
    ws=wb.create_sheet(name[:31]); r=1
    if banner:
        ws.cell(1,1,banner).font=Font(name='Arial',bold=True,color='FFFFFF'); 
        for c in range(1,max(len(headers),3)+1): ws.cell(1,c).fill=BAN
        r=2
    for j,h in enumerate(headers,1):
        c=ws.cell(r,j,h); c.font=Font(name='Arial',bold=True,color='FFFFFF'); c.fill=HF; c.alignment=Alignment(wrap_text=True,vertical='center')
    for i,row in enumerate(rows,r+1):
        for j,v in enumerate(row,1):
            if hasattr(v,'item'): v=v.item()
            if v!=v: v=None
            c=ws.cell(i,j,v); c.font=Font(name='Arial',size=10); c.alignment=Alignment(wrap_text=True,vertical='top'); c.border=Border(top=thin,bottom=thin,left=thin,right=thin)
    for j,h in enumerate(headers,1):
        w=(widths or {}).get(j) or min(48,max(12,len(str(h))+4,max([len(str(x[j-1])) for x in rows[:60]]+[0])*0.9))
        ws.column_dimensions[get_column_letter(j)].width=w
    ws.freeze_panes=ws.cell(r+1,1); ws.auto_filter.ref=f"A{r}:{get_column_letter(len(headers))}{r+len(rows)}"
    return ws,r
def readme(wb,lines):
    ws=wb.active; ws.title='README'
    for i,l in enumerate(lines,1):
        c=ws.cell(i,1,l); c.font=Font(name='Arial',size=11,bold=(i==1)); c.alignment=Alignment(wrap_text=True)
    ws.column_dimensions['A'].width=120
# ============ Workbook 1: Blueprint
wb=Workbook()
readme(wb,["VELOOP Task 01 - Analytics Blueprint (Deliverables 03,04,08,09,11,19,20 + coverage gaps)",
"STATUS: Every item is PROPOSED or TO BE VERIFIED. No item claims current VELOOP implementation. Nothing here is actual VELOOP data or performance.",
"Field-value lists marked 'observed' were seen in the SUPPLIED SIMULATED files only.",
"Sheets: Source_Register | Coverage_Matrix | Analytics_Gaps | User_Spec | Event_Plan | Data_Dictionary | KPI_Catalogue | KPI_Test | Assumptions | Backlog"])
sheet(wb,'Source_Register',['ID','Information','Source','Source Type','Date Checked','Status','Notes'],B.SOURCES)
sheet(wb,'Coverage_Matrix',['Product Area','Feature','User Action','System Action','Business Outcome','Data Required','Proposed Event','Source','Business Question','Status','Priority'],B.COV)
sheet(wb,'Analytics_Gaps',['Gap ID','Gap','Impact','Priority'],B.GAPS)
# user spec: from Users/Sessions dictionary rows + identifiers
uspec=[(r[1],r[2],r[5],r[4] if False else r[3],r[7],r[8],'Proposed') for r in B.DD if r[0] in('Users','Sessions')]
ident=[("user_id","Stable user identifier","Join users across every event and table"),("event_id","Unique event identifier","Deduplicate retried events"),("session_id","Session identifier","Group events into visits; compute duration"),("transaction_id","Wallet ledger identifier","Deduplicate/reconcile money movements; link reversals")]
sheet(wb,'User_Spec',['Field','Type','Required?','Purpose','Source','Validation','Status'],[(r[1],r[2],r[5],r[3],r[7],r[6],'Proposed') for r in B.DD if r[0] in('Users','Sessions')])
sheet(wb,'Event_Plan',['Event Name','Trigger','Definition','Common Fields (all events)','Required Properties','Optional Properties','Data Type','Validation','Source','Business Purpose','KPI Dependency','Domain','Priority','Implementation Status'],
 [(e[0],e[1],e[2],'event_id, user_id, timestamp (UTC), schema_version',e[3],e[4],'String/Timestamp/Decimal per Data_Dictionary',e[5],e[6],e[7],e[8],e[9],e[10],'Proposed - not verified in production') for e in B.EVENTS])
sheet(wb,'Data_Dictionary',['Entity','Field Name','Data Type','Definition','Example','Required','Allowed Values','Validation','Source','Sensitivity','Analytical Use','Status'],[r+('Proposed',) for r in B.DD])
sheet(wb,'KPI_Catalogue',['KPI ID','KPI Name','Definition','Formula','Required Fields','Data Source','Frequency','Stakeholder','Business Purpose','Interpretation','Limitation','Status','Group','Testability in this project'],[(k[0],k[1],k[2],k[3],k[4],k[5],k[6],k[7],k[8],k[9],k[10],k[11],k[12],B.TESTCLASS[k[0]]) for k in B.KPIS])
sheet(wb,'KPI_Test',['KPI ID','KPI Name','Testability','Why','Additional data needed'],B.kpi_test_rows())
sheet(wb,'Assumptions',['ID','Unknown','Why It Matters','Source Checked','Risk','Verification Owner','Status'],B.ASSUME)
sheet(wb,'Backlog',['Priority','Requirement','Reason','Dependency','Owner','Stage'],B.BACK)
rows=[('Product areas',F['n_areas']),('Features mapped (coverage rows)',F['n_features']),('Analytics gaps',F['n_gaps']),('Events in tracking plan',F['n_events']),('Proposed events also present in supplied data',F['n_proposed_seen']),('Data dictionary fields',F['n_fields']),('Entities',F['n_entities']),('KPIs',F['n_kpis']),('KPIs testable on supplied data',F['test']['Supplied data']),('KPIs partly testable',F['test']['Partly supplied']),('KPIs testable only on stand-in data',F['test']['Stand-in data only']),('KPIs with no data',F['test']['No data']),('Open assumptions',F['n_assume']),('Backlog items',F['n_backlog'])]
sheet(wb,'Report_Facts',['Fact','Value (same figure quoted in report and presentation)'],rows)
# summary counts with formulas
ws=wb['README']; r=7
ws.cell(r,1,"Counts (live formulas):").font=Font(name='Arial',bold=True)
ws.cell(r+1,1,'="Data dictionary fields: "&COUNTA(Data_Dictionary!B2:B500)')
ws.cell(r+2,1,'="Events in tracking plan: "&COUNTA(Event_Plan!A2:A500)')
ws.cell(r+3,1,'="KPIs in catalogue: "&COUNTA(KPI_Catalogue!A2:A500)')
ws.cell(r+4,1,'="Analytics gaps: "&COUNTA(Analytics_Gaps!A2:A500)')
ws.cell(r+5,1,'="Open assumptions: "&COUNTA(Assumptions!A2:A500)')
wb.save('/home/claude/repo/VELOOP_Task01_Blueprint.xlsx')
# ============ Workbook 2: Profiling & DQ
wb=Workbook(); BAN_T="SIMULATED DATA — CREATED FOR ANALYTICAL TESTING — NOT ACTUAL VELOOP DATA"
readme(wb,["VELOOP Task 01 - Simulated Data Profiling & Data Quality Audit (Deliverables 12, 13)",BAN_T,
"Sources: VELoop_Rewards_Data_01.xlsx (Task 01) and VELOOP_Simulated_User_Behavior_1000.xlsx (labelled 'Task 02'). Method: scripts/profile_data.py (pandas).",
"Rewards, Wallet, Withdrawals and Referrals were NOT supplied. The analyst generated labelled stand-ins (sheets SIM_* and DATA_*; see SIM_Methodology). Results on stand-ins are formula tests only.",
"Numbers describe the simulated files only. They are not VELOOP users, earnings, retention or performance."])
Pf=P.P.copy(); sheet(wb,'Dataset_Profile',list(Pf.columns),Pf.values.tolist(),BAN_T)
Cf=P.C.copy(); sheet(wb,'Field_Profile',list(Cf.columns),Cf.fillna('').values.tolist(),BAN_T)
sheet(wb,'Relationships',list(P.R.columns),P.R.values.tolist(),BAN_T)
ex=[(k,str(kk),vv) for k,v in P.extra.items() for kk,vv in v.items()]
sheet(wb,'Status_Distributions',['Distribution','Value','Count'],ex,BAN_T)
Qd=P.Q.drop_duplicates(subset=['dataset','field','issue_type']).copy()
Qd.loc[Qd.records_affected==0,'status']='Check passed - no issue found'
Qd.loc[Qd.records_affected==0,'severity']='Low'
Q=Qd.values.tolist()
ws,r=sheet(wb,'DQ_Issues',list(P.Q.columns),Q,BAN_T)
n=len(Q); s=wb['README']
s.cell(7,1,"Issue counts by severity (live formulas):").font=Font(name='Arial',bold=True)
for i,sv in enumerate(['Critical','High','Medium','Low']):
    s.cell(8+i,1,f'="{sv}: "&COUNTIF(DQ_Issues!F3:F{n+2},"{sv}")')
s.cell(12,1,f'="Total issues logged: "&COUNTA(DQ_Issues!A3:A{n+2})')
CB="CLEANING EVIDENCE ON SUPPLIED SIMULATED DATA — rules in scripts/clean_data.py"
sheet(wb,'Cleaning_Log',list(CD.LG.columns),CD.LG.values.tolist(),CB)
sheet(wb,'Before_After',list(CD.BA.columns),CD.BA.astype(object).values.tolist(),CB)
sheet(wb,'Cleaning_Validation',list(CD.VAL.columns),CD.VAL.values.tolist(),CB)
import pandas as _pd
cov=[(e[0],'Yes' if e[0] in set(F['proposed_seen']) else 'No',e[9],e[10]) for e in B.EVENTS]
sheet(wb,'Event_Coverage',['Proposed event','Present in supplied events?','Domain','Priority'],cov,"Compares the 39 proposed events with the 35 event names in the supplied simulated data")
prov=[('T01 Users_Clean / Users_Messy','Supplied','Users','Schema design, cleaning test, reference for validation','Numbers are simulated; not VELOOP users'),
('T02 Users, Sessions, Feature_Events, Daily_Activity, Task_Activity, Milestones','Supplied','Users, sessions, events, tasks','KPI formula tests, dashboard prototype, relationship tests','Numbers are simulated; category and reason mixes are near-uniform and carry no business signal'),
('T02 Event_Data_Quality_Audit','Supplied','Events with planted defects','Cleaning test','Planted defects'),
('SIM Rewards, Wallet_Transactions, Withdrawals, Referrals','Analyst-generated (scripts/generate_supplementary.py, seed 20261118)','Rewards, wallet, withdrawals, referrals','Testing joins, controls and KPI formulas only','Distributions are assumptions; replace with real data, never mix')]
sheet(wb,'Data_Provenance',['Dataset','Origin','Content','Allowed use','Limit'],prov,"WHICH DATA IS SUPPLIED AND WHICH IS ANALYST-GENERATED")
use=[('Event and field designs, KPI definitions, data model, quality controls, governance, backlog','Design','Usable for VELOOP once product facts are verified','They are specifications, not results'),
('Cleaning rules and the finding that count checks hide offsetting defects','Method','Usable','Method generalises to production data'),
('Need to remove direct identifiers (name, email) from the analytics layer','Finding on supplied files','Usable as design advice','Files are simulated but the principle holds'),
('Only 7 of 39 proposed events appear in the supplied event list; supplied names are feature-specific (for example ad_completed)','Finding on supplied files','Usable if VELOOP confirms the files mirror its event vocabulary','Confirm with engineering (A001)'),
('Rates such as task completion 57.2% or reversal 2.7%','Simulated results','NOT usable','Simulated or generated; formula tests only'),
('All reward, wallet, withdrawal and referral figures','Stand-in results','NOT usable','Analyst-generated assumptions')]
sheet(wb,'Findings_Usability',['Finding','Type','Can VELOOP use it?','Condition / reason'],use,"WHAT CAN AND CANNOT BE USED FOR VELOOP")
SB="SIMULATED DATA — ANALYST-GENERATED, NOT SUPPLIED, NOT ACTUAL VELOOP DATA"
sheet(wb,'SIM_Methodology',['Generation methodology'],[(l,) for l in GS.METHOD],SB,{1:140})
sheet(wb,'SIM_Profile',list(AS.PROF.columns),AS.PROF.astype(str).values.tolist(),SB)
sheet(wb,'SIM_Field_Profile',list(AS.FLD.columns),AS.FLD.fillna('').values.tolist(),SB)
sheet(wb,'SIM_Relationships',list(AS.REL.columns),AS.REL.values.tolist(),SB)
sheet(wb,'SIM_DQ_Checks',list(AS.SQ.columns),AS.SQ.values.tolist(),SB)
sheet(wb,'KPI_Formula_Tests',list(AS.KT.columns),AS.KT.astype(str).values.tolist(),"FORMULA TESTS ON SIMULATED DATA — NOT VELOOP PERFORMANCE")
for nm,df in GS.SIM.items():
    d=df.copy()
    for c_ in d.columns:
        if str(d[c_].dtype).startswith('datetime'): d[c_]=d[c_].dt.strftime('%Y-%m-%d %H:%M:%S')
    sheet(wb,'DATA_'+nm,list(d.columns),d.astype(object).where(d.notna(),None).values.tolist(),SB)
wb.save('/home/claude/repo/VELOOP_Task01_Data_Profiling_and_Quality.xlsx')
# cleaned datasets workbook
wc=Workbook(); readme(wc,['VELOOP Task 01 - Cleaned datasets (analytics-safe)','SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. Produced from the supplied messy sheets by scripts/clean_data.py.','Users: exact duplicates removed, malformed date blanked and flagged, missing required fields flagged (never imputed), name/email/gender removed, age banded.','Events: exact duplicates removed, text standardised to the controlled vocabulary.','Quarantine sheets hold the rejected rows. See Cleaning_Log and Before_After in the profiling workbook.'])
for nm,df in (('Users_Cleaned',CD.clean_users),('Events_Cleaned',CD.clean_events),('Users_Quarantine',CD.q_u),('Events_Quarantine',CD.q_e)):
    d=df.copy()
    for c_ in d.columns:
        if str(d[c_].dtype).startswith('datetime'): d[c_]=d[c_].dt.strftime('%Y-%m-%d %H:%M:%S')
    sheet(wc,nm,list(d.columns),d.astype(object).where(d.notna(),None).values.tolist(),'SIMULATED DATA — CLEANED OUTPUT')
wc.save('/home/claude/repo/VELOOP_Task01_Cleaned_Datasets.xlsx')
print('ok',n)

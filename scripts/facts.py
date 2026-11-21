"""Single source of truth for every count quoted in the report, workbooks and presentation."""
import json, collections
import blueprint_content as B
import profile_data as P
import analyze_supplementary as AS
import pandas as pd
F={}
F['n_areas']=len({r[0] for r in B.COV}); F['n_features']=len(B.COV); F['n_gaps']=len(B.GAPS)
F['n_events']=len(B.EVENTS); F['n_fields']=len(B.DD); F['n_entities']=len({r[0] for r in B.DD})
F['n_kpis']=len(B.KPIS); F['kpi_groups']=dict(collections.Counter(k[12] for k in B.KPIS))
F['n_assume']=len(B.ASSUME); F['n_backlog']=len(B.BACK); F['n_sources']=len(B.SOURCES)
tc=collections.Counter(B.TESTCLASS.values()); F['test']=dict(tc)
q=P.Q.drop_duplicates(subset=['dataset','field','issue_type'])
F['n_dq_checks']=len(q); F['n_dq_found']=int((q.records_affected>0).sum()); F['n_dq_passed']=int((q.records_affected==0).sum())
F['n_sq_checks']=len(AS.SQ); F['n_sq_found']=int((AS.SQ.records_affected>0).sum()); F['n_sq_planted']=int((AS.SQ.planted_in_generator>0).sum())
F['sq_detected_eq_planted']=int(((AS.SQ.planted_in_generator>0)&(AS.SQ.records_affected==AS.SQ.planted_in_generator)).sum())
ev=pd.read_csv('/home/claude/repo/data/cleaned/events_cleaned.csv'); obs=set(ev.event_name.unique()); prop={e[0] for e in B.EVENTS}
F['obs_event_names']=len(obs); F['proposed_seen']=sorted(prop&obs); F['n_proposed_seen']=len(prop&obs)
F['sizes']={'rewards':len(AS.S['Rewards']),'wallet':len(AS.S['Wallet_Transactions']),'withdrawals':len(AS.S['Withdrawals']),'referrals':len(AS.S['Referrals'])}
F.update(json.load(open('/home/claude/repo/scripts/facts_clean.json')))
F['kt']={r.kpi:r.simulated_test_value for r in AS.KT.itertuples()}
json.dump(F,open('/home/claude/repo/scripts/facts.json','w'),indent=1,default=str)
if __name__=='__main__': print(json.dumps(F,indent=1,default=str))

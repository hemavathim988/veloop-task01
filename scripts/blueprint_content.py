"""Content for VELOOP Task 01 blueprint. All entries are PROPOSED unless stated; nothing here asserts current VELOOP implementation."""
# ---------- Source & verification register
SOURCES=[
("S001","Assignment brief lists intended product areas (accounts, VEs, XP, Gems, Tokens, Spins, daily rewards, streaks, tasks, missions, badges, levels, referrals, wallet, exchange, withdrawals, support)","Data_Analyst_01 brief (PDF)","Internal","2026-11-19","To Be Verified","Brief says not every feature is implemented or production-ready"),
("S002","Simulated Users dataset (1,000 users + messy audit sheet) exists for Task 01","VELoop_Rewards_Data_01.xlsx","Simulated","2026-11-19","Confirmed (file exists; data is fictional)","Contains only Users; README marks it SIMULATED / FICTIONAL"),
("S003","Behaviour dataset (sessions, events, daily activity, tasks, milestones) supplied","VELOOP_Simulated_User_Behavior_1000.xlsx","Simulated","2026-11-19","Confirmed (file exists; data is fictional)","README names it 'Task 02'; same user_ids as Task 01 but conflicting attributes"),
("S004","Rewards, Wallet, Withdrawals, Referrals datasets were not supplied","Not in either uploaded workbook","Simulated","2026-11-19","Confirmed (absence)","Analyst generated labelled replacements (scripts/generate_supplementary.py); real sheets from the brief's Drive folder should replace them"),
("S007","Analyst-generated simulated Rewards, Wallet_Transactions, Withdrawals, Referrals","scripts/generate_supplementary.py (seed 20261118)","Simulated","2026-11-19","Confirmed (generated; fictional)","Distributions are assumptions, not VELOOP behaviour; methodology in profiling workbook"),
("S005","Official product/engineering documentation (event emission, IDs, schemas, withdrawal rules)","Not available to the analyst","Official","2026-11-21","To Be Verified","Only the public About Us page was reviewed (S008); engineering facts remain unverified"),
("S008","VELOOP Rewards describes itself as an online-operated rewards and engagement platform based in India that uses internal digital units such as VEs, XP, Gems, Tokens, Spins and badges","https://www.velooprewards.in/about-us","Official","2026-11-21","Confirmed (as stated by the official site; implementation and which units are live not verified)","Public marketing text, not product documentation"),
("S009","The official About Us page lists withdrawal concerns among the topics handled by support channels","https://www.velooprewards.in/about-us","Official","2026-11-21","Confirmed (that withdrawals are referenced); methods, states and timings To Be Verified","Does not describe the withdrawal lifecycle"),
("S010","The public homepage shows user-count and payout-total figures","https://www.velooprewards.in/","Official","2026-11-21","To Be Verified - NOT USED","Marketing figures cannot be verified and sit awkwardly with the brief's statement that production volume is low; no figure from the site is used anywhere in this work"),
("S011","Public GitHub repositories named VELOOP (landing pages, giveaway demos)","GitHub search","Internal","2026-11-21","Not used","Other people's demo projects, not official documentation; their features are not evidence of VELOOP behaviour"),
("S006","Current backend event emission, IDs, session handling, idempotency","Not reviewed","Internal","2026-11-19","To Be Verified","Needs engineering confirmation (see Assumption Register)"),
]
# ---------- Coverage matrix: area,feature,user action,system action,business outcome,data required,proposed event,source,business question,status,priority
COV=[
("Account","Registration","User submits sign-up","Account created, user_id issued","New user","user_id, registered_at, acquisition_source, platform, device","user_registered","Backend","How many users join and from where?","Proposed","Critical"),
("Account","Login","User logs in","Session started","Returning activity","user_id, session_id, login_at, platform","user_logged_in","Backend","Who returns and how often?","Proposed","Critical"),
("Account","Onboarding","User starts/finishes onboarding","Milestone stored","Activated user","onboarding_step, started_at, completed_at","onboarding_started / onboarding_completed","Frontend+Backend","Where do users drop off?","Proposed","High"),
("Account","Account lifecycle","-","Status changed (active/suspended/inactive)","Lifecycle state","account_status, status_changed_at, reason_category","account_status_changed","Backend","How many accounts are suspended or inactive?","Proposed","High"),
("Tasks","Task system","View, open, start, complete task","Validation, completion recorded","Completed task","task_id, task_type, status, validation_status","task_viewed/opened/started/completed/failed","Frontend+Backend","What is the funnel from view to validated completion?","Proposed","Critical"),
("Tasks","Third-party offers/ads/surveys","User watches ad / does survey","Partner confirms or fails","Externally dependent completion","provider, provider_ref, partner_status","task_completed (with provider fields)","Backend","How much outcome depends on partners?","To Be Verified","High"),
("Rewards","Reward crediting","-","Reward pending/credited/reversed","Value delivered","reward_id, amount, unit, status, task_ref","reward_pending / reward_credited / reward_reversed","Backend","Is activity actually rewarded?","Proposed","Critical"),
("Engagement","Daily reward & streaks","Claim daily reward","Streak updated","Habit formed","claim_at, streak_count","daily_reward_claimed / streak_updated","Backend","Do streaks improve retention?","Proposed","Medium"),
("Engagement","Missions & badges","Start/finish mission","Badge awarded","Progression","mission_id, badge_id","mission_started/completed, badge_earned","Backend","Which missions get finished?","Proposed","Medium"),
("Engagement","Spin","Open and spin","Prize decided","Reward outcome","spin_id, prize_unit, prize_amount","spin_started / spin_completed","Backend","How is spin used?","Proposed","Medium"),
("Engagement","Tap & Earn / Mining","Tap or start mining","Accrual recorded","Passive/active earning","session_ref, accrued_amount","tap_completed, mining_started/stopped (extra proposed)","Backend","Which earning feature is most used?","To Be Verified","Medium"),
("Referrals","Referral program","Share code, friend registers","Link referral to user, activate","Converted referral","referral_id, referrer_id, referred_id, timestamps, status","referral_created/registered/activated/converted","Backend","Does registration become real conversion?","Proposed","High"),
("Wallet","Wallet ledger","-","Transaction recorded","Balance change","transaction_id, type, amount, unit, status, reference_id","wallet_transaction_created/completed/reversed","Backend","Do balances reconcile?","Proposed","Critical"),
("Wallet","Exchange","Convert units","Exchange transaction","Redemption","from_unit,to_unit,rate_ref","wallet_transaction_created (type=exchange, Proposed)","Backend","How do users convert value?","To Be Verified","Medium"),
("Withdrawals","Withdrawal lifecycle","Request withdrawal","Review, process, complete/reject/reverse","Payout outcome","withdrawal_id, amount, method, timestamps, status, reason_category","withdrawal_requested/processing/completed/rejected/reversed","Backend","How long does payout take; what is pending?","Proposed","Critical"),
("Support","Help Center","View article / raise ticket","Ticket created","Support load","ticket_id, category, status","support_ticket_created, help_article_viewed","Frontend+Backend","What issues do users have?","To Be Verified","Medium"),
("Platform","Sessions","Open/close app","Session start/end","Usage time","session_id, start, end","session_started / session_ended","Frontend","How long do users stay?","Proposed","High"),
]
GAPS=[
("G01","No stable transaction_id evidenced for wallet","Cannot deduplicate wallet transactions","Critical"),
("G02","Rewards, Wallet, Withdrawals, Referrals datasets absent from supplied workbooks (analyst-generated stand-ins used for testing)","Money KPIs tested only on stand-in data, not supplied data","Critical"),
("G03","Task funnel stages (opened vs started) not distinguished in supplied events","Funnel drop-off unmeasurable between view and start","High"),
("G04","Reward status exists on tasks but no reward amount/unit columns","Reward value KPIs not computable","Critical"),
("G05","No reward_reversed / correction linkage in supplied data","Reversals cannot be tied to originals","High"),
("G06","Two supplied workbooks disagree on user attributes for identical user_ids","Cross-file joins give wrong attributes","High"),
("G07","Direct personal data (name, email, gender, age, city) in analytic datasets","Privacy risk; not needed for KPIs","High"),
("G08","Sessions table has session_status only 'Completed' (7,913/7,913)","Cannot measure crashed/abandoned sessions","Medium"),
("G09","No acquisition campaign/UTM detail beyond source category","Acquisition quality unmeasurable","Medium"),
("G10","No timezone defined on timestamps","Daily metrics may shift by timezone","High"),
("G11","No event schema version or idempotency key","Duplicate events (10 seen in audit sheet) cannot be reliably removed","High"),
("G12","Third-party/partner status not captured on tasks","Cannot separate VELOOP failures from partner failures","High"),
("G13","No withdrawal reason categories or timestamps","Processing time and rejection analysis impossible","Critical"),
("G14","Referral activation definition undefined","Conversion KPI ambiguous","High"),
]
# ---------- Event plan  (event, trigger, definition, props_required, props_optional, validation, source, purpose, kpi, domain, priority)
ID=["event_id","user_id","timestamp"]
EVENTS=[
("user_registered","Account creation committed","User account created","registration_source, platform, device_type","campaign_ref","user_id unique; registration_source in controlled list","Backend","Registrations","KPI-U01","Account","Critical"),
("user_logged_in","Successful authentication","Session authenticated","session_id, platform, device_type","","session_id non-null","Backend","Returning users","KPI-U03","Account","Critical"),
("user_logged_out","Explicit logout","User ended session manually","session_id","","Only where logout exists","Frontend","Session length","KPI-U04","Account","Low"),
("onboarding_started","First onboarding screen shown","Onboarding began","onboarding_version","","once per user per version","Frontend","Activation funnel","KPI-U05","Account","High"),
("onboarding_completed","Final step confirmed","Onboarding finished","onboarding_version, duration_seconds","","duration>=0","Backend","Activation rate","KPI-U05","Account","High"),
("account_status_changed","Status field changes","Lifecycle change","old_status, new_status","reason_category","old!=new; both in allowed values","Backend","Lifecycle","KPI-U06","Account","High"),
("session_started","App/session opened","Session began","session_id, platform, entry_point","","session_id unique","Frontend","Usage","KPI-E01","Platform","High"),
("session_ended","Session closed/timeout","Session ended","session_id, duration_seconds","exit_feature","end>=start","Frontend","Time spent","KPI-E02","Platform","Medium"),
("task_viewed","Task card displayed","Task shown to user","task_id, task_type, feature","","task_id exists in catalogue","Frontend","Funnel top","KPI-E03","Tasks","High"),
("task_opened","User opens task detail","Task opened","task_id, task_type","","after task_viewed","Frontend","Interest","KPI-E03","Tasks","Medium"),
("task_started","User begins action","Task attempt began","task_id, task_type, attempt_id","provider","attempt_id unique","Backend","Starts","KPI-E04","Tasks","Critical"),
("task_completed","Completion passed validation","Validated completion","task_id, task_type, attempt_id, status, reward_amount, reward_unit","provider_ref","exactly one per attempt","Backend","Completions","KPI-E05","Tasks","Critical"),
("task_failed","Attempt ended unsuccessfully","Failure recorded","task_id, attempt_id, failure_category","provider_error_ref","failure_category in proposed list","Backend","Failure analysis","KPI-E06","Tasks","Critical"),
("task_abandoned","User exits before completion","Abandonment","task_id, attempt_id","last_step","after task_started","Frontend","Abandon rate","KPI-E07","Tasks","Medium"),
("reward_pending","Reward awaiting validation","Reward queued","reward_id, amount, unit, source_ref","expected_at","amount>0","Backend","Pending value","KPI-R03","Rewards","High"),
("reward_credited","Reward posted to wallet","Reward credited","reward_id, amount, unit, source_ref, transaction_id","","exactly one credit per reward_id","Backend","Credits","KPI-R01","Rewards","Critical"),
("reward_reversed","Credit undone","Reward reversed","reward_id, original_reward_id, amount, unit, reason_category","","references existing credit","Backend","Reversal rate","KPI-R04","Rewards","Critical"),
("reward_corrected","Amount adjusted","Reward corrected","reward_id, old_amount, new_amount, reason_category","","old!=new","Backend","Accuracy","KPI-R05","Rewards","Medium"),
("daily_reward_claimed","Daily claim success","Daily reward claimed","claim_date, amount, unit","","one per user per day","Backend","Habit","KPI-E08","Engagement","Medium"),
("streak_updated","Streak changes","Streak value changed","old_streak, new_streak","","new>=0","Backend","Streaks","KPI-E09","Engagement","Medium"),
("mission_started","Mission accepted","Mission begun","mission_id","","mission exists","Backend","Mission funnel","KPI-E10","Engagement","Medium"),
("mission_completed","Mission criteria met","Mission finished","mission_id","reward_id","after mission_started","Backend","Completion","KPI-E10","Engagement","Medium"),
("badge_earned","Badge awarded","Badge granted","badge_id","","once per badge per user","Backend","Progression","KPI-E11","Engagement","Low"),
("spin_started","Spin initiated","Spin began","spin_id","","unique spin_id","Backend","Usage","KPI-E12","Engagement","Medium"),
("spin_completed","Spin result delivered","Spin finished","spin_id, prize_amount, prize_unit","","after spin_started","Backend","Outcome","KPI-E12","Engagement","Medium"),
("referral_created","Referral code/link generated for a referee","Referral record created","referral_id, referrer_id","channel","referral_id unique","Backend","Referral top","KPI-F01","Referrals","High"),
("referral_registered","Referred user registers","Referee registered","referral_id, referred_user_id","","referred!=referrer","Backend","Registrations","KPI-F02","Referrals","High"),
("referral_activated","Referee meets activation rule (rule To Be Verified)","Referee active","referral_id, activation_rule","","rule defined","Backend","Activation","KPI-F03","Referrals","High"),
("referral_converted","Conversion condition met","Referral converted","referral_id, conversion_rule","","after activated","Backend","Conversion","KPI-F04","Referrals","High"),
("wallet_transaction_created","Ledger entry created","Transaction created","transaction_id, type, amount, unit, status, reference_id","","transaction_id unique","Backend","Ledger","KPI-W01","Wallet","Critical"),
("wallet_transaction_completed","Entry settled","Transaction completed","transaction_id","","after created","Backend","Settlement","KPI-W02","Wallet","Critical"),
("wallet_transaction_reversed","Entry reversed","Transaction reversed","transaction_id, original_transaction_id, reason_category","","original exists","Backend","Reversals","KPI-W04","Wallet","Critical"),
("withdrawal_requested","User requests payout","Withdrawal requested","withdrawal_id, amount, unit, method","","amount>0","Backend","Requests","KPI-D01","Withdrawals","Critical"),
("withdrawal_processing","Review/processing starts","Under review","withdrawal_id","queue_ref","after requested","Backend","Queue","KPI-D03","Withdrawals","Critical"),
("withdrawal_completed","Payout completed","Completed","withdrawal_id, method","","after processing","Backend","Completions","KPI-D02","Withdrawals","Critical"),
("withdrawal_rejected","Request rejected","Rejected","withdrawal_id, reason_category","","reason in proposed list","Backend","Rejections","KPI-D04","Withdrawals","Critical"),
("withdrawal_reversed","Completed payout reversed","Reversed","withdrawal_id, reason_category","","after completed","Backend","Reversals","KPI-D05","Withdrawals","High"),
("help_article_viewed","Help article opened","Help engagement","article_id","","","Frontend","Content KPI","KPI-S03","Support","Low"),
("support_ticket_created","Ticket opened","Support request","ticket_id, issue_category","","ticket_id unique","Backend","Support load","KPI-S01","Support","Medium"),
]
# ---------- Data dictionary (entity, field, type, definition, example, required, allowed, validation, source, sensitivity, use)
def D(ent,rows,src='Backend'):
    return [(ent,)+r[:5]+(r[5],r[6],src,r[7],r[8]) for r in rows]
DD=[]
DD+=D("Users",[
("user_id","String","Stable pseudonymous user identifier","USR000123","Yes","unique","Non-null, unique, immutable","Restricted","Join key across all entities"),
("registered_at","Timestamp (UTC)","Account creation time","2026-06-10T07:14:00Z","Yes","","ISO-8601 UTC; <= now","Internal","Cohorts, lifecycle"),
("acquisition_source","String","Channel category at sign-up","Organic Search","Yes","Organic Search; Direct; Social Media; Referral; WhatsApp; Telegram; Other (observed in simulated data)","In allowed list","Internal","Acquisition analysis"),
("referral_source_detail","String","Detail when source is Referral","Friend/Family","Conditional","Required if source=Referral","Conditional rule","Internal","Referral quality"),
("platform","String","Client platform","Web","Yes","Web (only value observed)","In allowed list","Internal","Platform split"),
("primary_device","String","Main device type","Android","Yes","Android; iOS; Windows; macOS (observed)","In allowed list","Internal","Device mix"),
("account_status","String","Current lifecycle status","Active","Yes","Active; Inactive; Suspended; Pending Verification (observed)","In allowed list","Internal","Lifecycle KPIs"),
("email_verification_status","String","Verification state (no email stored)","Verified","Yes","Verified; Pending","In allowed list","Internal","Activation"),
("onboarding_status","String","Onboarding progress","Completed","Yes","Not Started; Started; Completed","In allowed list","Internal","Onboarding funnel"),
("last_active_at","Timestamp (UTC)","Last qualifying activity","2026-09-01T10:00:00Z","No","","Null means never active","Internal","Inactive users"),
("consent_status","String","Data-use consent state","Accepted","Yes","Accepted; Pending","In allowed list","Restricted","Governance"),
("country_code","String","ISO country code","IN","No","ISO-3166","2 letters","Internal","Geography (coarse)"),
])
DD+=D("Sessions",[
("session_id","String","Unique session identifier","SESS0000001","Yes","","Unique","Internal","Session grouping"),
("user_id","String","FK to Users","USR000123","Yes","","Exists in Users","Restricted","Join"),
("session_start","Timestamp (UTC)","Session start","2026-08-11T10:30:01Z","Yes","","<= session_end","Internal","Duration"),
("session_end","Timestamp (UTC)","Session end","2026-08-11T10:30:46Z","No","","Null if open","Internal","Duration"),
("entry_point","String","Where session began","Home","No","Home; Help/Support; ...","Controlled list","Internal","Navigation"),
("session_status","String","Outcome of session","Completed","Yes","Completed; Abandoned (Proposed)","Controlled list","Internal","Session health"),
])
DD+=D("Tasks",[
("task_id","String","Catalogue identifier of a task","TASK0071","Yes","","Unique in catalogue","Internal","Task joins"),
("task_category","String","Type of task","Survey","Yes","Advertisement; App Task; CAPTCHA; Game; Mission; Promotional Task; Social Activity; Survey (observed)","Controlled list","Internal","Mix analysis"),
("provider","String","External partner, if any","(To Be Verified)","No","","Controlled list","Internal","Partner dependency"),
("task_reward_unit","String","Unit paid by task","VE","No","VE; XP; Gems; Tokens (Proposed)","Controlled list","Internal","Reward mix"),
])
DD+=D("Task_Activity",[
("activity_id","String","One attempt record (attempt_id)","ACT0000001","Yes","","Unique","Internal","Idempotency"),
("user_id","String","FK to Users","USR000980","Yes","","Exists","Restricted","Join"),
("task_id","String","FK to Tasks","TASK0071","Yes","","Exists","Internal","Join"),
("task_viewed_at","Timestamp (UTC)","Task shown","2026-08-05T19:36:29Z","Yes","","<= started","Internal","Funnel"),
("task_started_at","Timestamp (UTC)","Attempt began","2026-08-05T19:38:50Z","No","","<= completed","Internal","Funnel"),
("task_completed_at","Timestamp (UTC)","Validated completion","","No","","Non-null iff status=Completed","Internal","Completion time"),
("task_status","String","Attempt outcome","Failed","Yes","Completed; Abandoned; Failed; Pending (observed)","State machine","Internal","Completion rate"),
("failure_reason","String","Failure category","Timeout","Conditional","Validation failed; Task unavailable; Timeout; Incomplete action; User exited (observed)","Required if Failed/Abandoned","Internal","Failure analysis"),
("validation_status","String","Result of validation","Passed","No","Passed; Failed; Pending (Proposed)","Controlled list","Internal","Trust in completion"),
("session_id","String","FK to Sessions","SESS0007786","No","","Exists","Internal","Context"),
])
DD+=D("Rewards",[
("reward_id","String","Unique reward record","RWD000001","Yes","","Unique","Internal","Dedup"),
("user_id","String","FK to Users","USR000123","Yes","","Exists","Restricted","Join"),
("activity_id","String","FK to Task_Activity (source)","ACT0000001","No","","Exists if present","Internal","Attribution"),
("reward_amount","Decimal","Amount","25","Yes","","> 0","Internal","Credit volume"),
("reward_unit","String","Unit","VE","Yes","VE; XP; Gems; Tokens (Proposed)","Controlled list","Internal","Per-unit totals"),
("reward_status","String","Credit state","Credited","Yes","Pending; Credited; Not Credited; Reversed; Corrected","State machine","Internal","Reward KPIs"),
("reward_created_at","Timestamp (UTC)","When queued","2026-08-05T19:40:00Z","Yes","","ISO-8601","Internal","Latency"),
("reward_credited_at","Timestamp (UTC)","When posted","2026-08-05T19:41:00Z","No","","Non-null iff Credited","Internal","Latency"),
("original_reward_id","String","Link for reversal/correction","RWD000001","No","","Exists","Internal","Reversal tracing"),
])
DD+=D("Wallet_Transactions",[
("transaction_id","String","Unique ledger entry","TXN000001","Yes","","Unique, immutable","Internal","Deduplication"),
("user_id","String","FK to Users","USR000123","Yes","","Exists","Restricted","Join"),
("transaction_type","String","Kind of entry","reward_credit","Yes","reward_credit; redemption; reversal; adjustment; exchange (all Proposed)","Controlled list","Internal","Ledger mix"),
("amount","Decimal","Signed or absolute amount (rule to confirm)","25","Yes","","Numeric","Internal","Volume"),
("unit","String","Unit","VE","Yes","VE; XP; Gems; Tokens","Controlled list","Internal","Per-unit"),
("transaction_status","String","State","Completed","Yes","Created; Completed; Reversed; Failed","State machine","Internal","Settlement"),
("reference_id","String","Source object ID (reward/withdrawal)","RWD000001","Yes","","Exists","Internal","Reconciliation"),
("related_transaction_id","String","Link to reversed/corrected entry","TXN000000","No","","Exists","Internal","Reversal tracing"),
("created_at","Timestamp (UTC)","Entry time","2026-08-05T19:41:00Z","Yes","","ISO-8601","Internal","Trends"),
])
DD+=D("Withdrawals",[
("withdrawal_id","String","Unique withdrawal","WDR000001","Yes","","Unique","Internal","Dedup"),
("user_id","String","FK to Users","USR000123","Yes","","Exists","Restricted","Join"),
("requested_amount","Decimal","Requested amount","500","Yes","","> 0","Internal","Volume"),
("amount_unit","String","Unit/currency","INR (To Be Verified)","Yes","","Controlled list","Internal","Volume"),
("method","String","Payout method category","UPI (To Be Verified)","Yes","Not defined - To Be Verified","Controlled list; no account details","Internal","Method mix"),
("requested_at","Timestamp (UTC)","Request time","2026-09-01T09:00:00Z","Yes","","ISO-8601","Internal","Queue age"),
("processing_started_at","Timestamp (UTC)","Review start","","No","","> requested_at","Internal","Processing time"),
("final_at","Timestamp (UTC)","Final state time","","No","","> requested_at","Internal","Processing time"),
("withdrawal_status","String","State","Pending","Yes","Requested; Processing; Completed; Rejected; Reversed","State machine","Internal","Status KPIs"),
("reason_category","String","Rejection/reversal reason class","(Proposed)","Conditional","Proposed list only","Required if Rejected/Reversed","Internal","Root cause"),
])
DD+=D("Referrals",[
("referral_id","String","Unique referral","REF000001","Yes","","Unique","Internal","Dedup"),
("referrer_user_id","String","FK to Users","USR000123","Yes","","Exists","Restricted","Join"),
("referred_user_id","String","FK to Users (after registration)","USR000456","No","","Exists; != referrer","Restricted","Join"),
("created_at","Timestamp (UTC)","Referral created","2026-07-01T10:00:00Z","Yes","","ISO-8601","Internal","Funnel"),
("registered_at","Timestamp (UTC)","Referee registered","","No","","> created_at","Internal","Funnel"),
("activated_at","Timestamp (UTC)","Referee activated","","No","","> registered_at","Internal","Funnel"),
("referral_status","String","Funnel state","Registered","Yes","Created; Registered; Activated; Converted; Expired","State machine","Internal","Conversion"),
("referral_channel","String","How shared","WhatsApp","No","Controlled list","In list","Internal","Channel quality"),
])
DD+=D("Feature_Events",[
("event_id","String","Unique event ID (idempotency key)","EVT00000001","Yes","","Unique","Internal","Deduplication"),
("user_id","String","FK to Users","USR000123","Yes","","Exists","Restricted","Join"),
("session_id","String","FK to Sessions","SESS0000001","No","","Exists","Internal","Sequencing"),
("event_name","String","Event in object_action form","task_completed","Yes","See Event_Plan","In catalogue","Internal","Core metric basis"),
("feature_name","String","Feature the event belongs to","Watch Ads","Yes","Controlled vocabulary (15 values observed)","Exact-match case","Internal","Feature usage"),
("event_timestamp","Timestamp (UTC)","When event occurred","2026-08-11T10:30:03Z","Yes","","ISO-8601 UTC","Internal","Time series"),
("event_status","String","Outcome stage","Success","Yes","Started; Success; Abandoned; Failed (observed)","Exact-match case, trimmed","Internal","Success rates"),
("schema_version","String","Event schema version","1.0","Yes","","semver","Internal","Change management"),
("sequence_number","Integer","Order within session","3","No","","> 0","Internal","Path analysis"),
])
DD+=D("Support_Tickets",[
("ticket_id","String","Unique ticket","TCK000001","Yes","","Unique","Internal","Dedup"),
("user_id","String","FK to Users","USR000123","Yes","","Exists","Restricted","Join"),
("issue_category","String","Issue class","Withdrawal delay (Proposed)","Yes","Proposed list","Controlled list","Internal","Issue mix"),
("ticket_status","String","State","Open","Yes","Open; Resolved","Controlled list","Internal","Support load"),
("created_at","Timestamp (UTC)","Opened","2026-09-02T08:00:00Z","Yes","","ISO-8601","Internal","Trends"),
])
# ---------- KPIs  (id,name,def,formula,fields,source,freq,stakeholder,purpose,interpretation,limitation,status,group)
K=[]
def k(i,n,d,f,fl,s,fr,st,p,it,lim,g): K.append((i,n,d,f,fl,s,fr,st,p,it,lim,"Proposed",g))
k("KPI-U01","Registrations","Count of accounts created in period","COUNT(user_id) WHERE registered_at in period","user_id, registered_at","Users","Daily","Product","Growth intake","Rising = more sign-ups; interpret with source mix","Counts accounts, not real people","User")
k("KPI-U02","Daily Active Users (DAU)","Unique users with a qualifying activity event in a calendar day","COUNT(DISTINCT user_id) WHERE qualifying event on date","user_id, event_timestamp, event_name","Feature_Events","Daily","Product","Usage","Compare to MAU for stickiness","Depends on qualifying-event definition and timezone","User")
k("KPI-U03","Returning Users","Active users in period who were also active in an earlier period","COUNT(DISTINCT user_id active now AND active before)","user_id, event_timestamp","Feature_Events","Weekly","Product","Retention signal","Higher = repeat use","Needs lookback window definition","User")
k("KPI-U04","Average Session Duration","Mean session length","AVG(session_end - session_start)","session_start, session_end","Sessions","Weekly","Product","Depth of use","Longer is not always better","Open sessions bias","User")
k("KPI-U05","Onboarding Completion Rate","Share of users who started onboarding and completed it","completed / started","onboarding events","Events","Weekly","Product","Activation","Low = friction","Requires both events","User")
k("KPI-U06","Inactive Users","Users with no qualifying activity in N days","COUNT users WHERE last_active_at < today-N","last_active_at","Users","Weekly","Product/Ops","Churn risk","Track trend","N undefined (To Be Verified)","User")
k("KPI-U07","Suspended Accounts","Accounts with status Suspended","COUNT WHERE account_status='Suspended'","account_status","Users","Weekly","Operations","Risk","Watch growth","Reason not captured","User")
k("KPI-U08","Email Verification Rate","Verified / registered","verified / registered","email_verification_status","Users","Weekly","Product","Trust","Low = verification friction","Depends on policy","User")
k("KPI-E01","Sessions per Active User","Sessions divided by active users","COUNT(sessions)/COUNT(DISTINCT active users)","session_id, user_id","Sessions","Daily","Product","Frequency","Higher = habit","Sessions may be inflated by reconnects","Engagement")
k("KPI-E02","Feature Adoption Rate","Users who used a feature / active users","distinct users with feature event / distinct active users","feature_name, user_id","Feature_Events","Weekly","Product","Feature value","Low = discoverability","Feature list may change","Engagement")
k("KPI-E03","Task Views","Task viewed events","COUNT task_viewed","task events","Feature_Events/Task_Activity","Daily","Product","Funnel top","Context for conversion","Needs task_viewed instrumentation","Engagement")
k("KPI-E04","Task Starts","Attempts started","COUNT task_started","task_started_at","Task_Activity","Daily","Product","Intent","Compare with views","Open vs start not separated in sample","Engagement")
k("KPI-E05","Task Completions","Validated completions","COUNT task_status='Completed'","task_status","Task_Activity","Daily","Product","Output","Trend by category","Validation definition To Be Verified","Engagement")
k("KPI-E06","Task Completion Rate","Completed / started","COUNT Completed / COUNT started","status, started_at","Task_Activity","Daily","Product","Efficiency","Low = friction or partner issues","Pending attempts distort recent days","Engagement")
k("KPI-E07","Task Abandonment Rate","Abandoned / started","COUNT Abandoned / COUNT started","status","Task_Activity","Weekly","Product","Friction","High = UX/offer problem","User-exit definition needed","Engagement")
k("KPI-E08","Daily Reward Claim Rate","Users claiming daily reward / active users","COUNT claim users / COUNT active users","daily_reward_claimed","Events","Daily","Product","Habit","Higher = habit","Feature status To Be Verified","Engagement")
k("KPI-E09","Streak Retention","Users with streak >= N / users who started a streak","COUNT streak>=N / COUNT streak users","streak_count","Events","Weekly","Product","Retention","Longer streaks = stickier","N undefined","Engagement")
k("KPI-E10","Mission Completion Rate","mission_completed / mission_started","ratio","mission events","Events","Weekly","Product","Progression","Low = hard missions","Event coverage","Engagement")
k("KPI-E11","Badges Earned per Active User","badge_earned count / active users","ratio","badge_earned","Events","Weekly","Product","Progression","Context only","Feature status To Be Verified","Engagement")
k("KPI-E12","Spin Completion Rate","spin_completed / spin_started","ratio","spin events","Events","Weekly","Product","Feature health","Low = drop-off","Feature status To Be Verified","Engagement")
k("KPI-R01","Reward Credits","Count of reward_credited","COUNT reward_status='Credited'","reward_status","Rewards","Daily","Finance/Product","Delivery","Compare with completions","Needs Rewards table","Reward")
k("KPI-R02","Reward Credit Volume by Unit","Sum of credited amounts per unit","SUM(reward_amount) GROUP BY unit WHERE Credited","amount, unit","Rewards","Daily","Finance","Value delivered","Never sum across units","Needs Rewards table","Reward")
k("KPI-R03","Pending Rewards","Rewards awaiting credit","COUNT status='Pending'","reward_status","Rewards","Daily","Operations","Backlog","Rising = validation delays","Needs Rewards table","Reward")
k("KPI-R04","Reward Reversal Rate","Reversed / credited","COUNT Reversed / COUNT Credited","reward_status","Rewards","Weekly","Finance","Integrity","High = quality problem","Reason categories Proposed","Reward")
k("KPI-R05","Reward Corrections","Count of corrected rewards","COUNT Corrected","reward_status","Rewards","Weekly","Finance","Accuracy","Low expected","Needs correction events","Reward")
k("KPI-R06","Reward Activity by Feature","Credits per feature","COUNT credited GROUP BY feature/task_category","task_category, status","Rewards+Task_Activity","Weekly","Product","Mix","Shows value source","Needs reward-to-activity link","Reward")
k("KPI-R07","Activity-to-Credit Ratio","Credited rewards / completed activities","credited / completed","activity_id, reward_status","Task_Activity+Rewards","Weekly","Product/Finance","Leakage detection","Ratio far from 1 = mismatch","Needs link key","Reward")
k("KPI-W01","Wallet Transactions","Count of wallet entries","COUNT transaction_id","transaction_id","Wallet","Daily","Finance","Ledger volume","Context","Needs Wallet table","Wallet")
k("KPI-W02","Wallet Credit Volume","Sum of credit-type amounts per unit","SUM(amount) WHERE type credit GROUP BY unit","amount, type, unit","Wallet","Daily","Finance","Inflow","Per unit only","Needs Wallet table","Wallet")
k("KPI-W03","Redemption Activity","Count/volume of redemption entries","COUNT/SUM type='redemption'","type, amount","Wallet","Weekly","Finance","Outflow","Context","Type list Proposed","Wallet")
k("KPI-W04","Wallet Reversal Rate","Reversed entries / completed entries","COUNT Reversed / COUNT Completed","status","Wallet","Weekly","Finance","Integrity","High = issue","Needs related_transaction_id","Wallet")
k("KPI-D01","Withdrawal Requests","Count of withdrawals requested","COUNT withdrawal_id","withdrawal_id","Withdrawals","Daily","Operations","Demand","Trend","Needs Withdrawals table","Withdrawal")
k("KPI-D02","Completed Withdrawals","Count status Completed","COUNT Completed","status","Withdrawals","Daily","Operations","Delivery","Compare to requests","Needs Withdrawals table","Withdrawal")
k("KPI-D03","Pending Withdrawal Queue","Count still Requested/Processing","COUNT status IN (Requested, Processing)","status","Withdrawals","Daily","Operations","Backlog","Rising = delays","Needs Withdrawals table","Withdrawal")
k("KPI-D04","Rejected Withdrawals","Count Rejected","COUNT Rejected","status","Withdrawals","Weekly","Operations","Friction","Check reasons","Reason categories Proposed","Withdrawal")
k("KPI-D05","Reversed Withdrawals","Count Reversed","COUNT Reversed","status","Withdrawals","Weekly","Finance","Integrity","Low expected","Needs Withdrawals table","Withdrawal")
k("KPI-D06","Median Processing Time","Median(final_at - requested_at) for Completed","MEDIAN","timestamps","Withdrawals","Weekly","Operations","Service level","Lower = faster","Excludes open items (survivorship)","Withdrawal")
k("KPI-D07","Withdrawal Completion Rate","Completed / (Completed+Rejected+Reversed)","ratio over closed requests","status","Withdrawals","Weekly","Operations","Outcome","Use closed requests only","Pending excluded","Withdrawal")
k("KPI-D08","Withdrawal Method Distribution","Share of requests per method","COUNT per method / total","method","Withdrawals","Weekly","Product","Method planning","Context","Methods undefined","Withdrawal")
k("KPI-F01","Referrals Created","Count referrals","COUNT referral_id","referral_id","Referrals","Daily","Growth","Top of funnel","Context","Needs Referrals table","Referral")
k("KPI-F02","Referral Registrations","Referrals with registered_at","COUNT registered_at not null","registered_at","Referrals","Daily","Growth","Funnel","Compare with created","Not conversion","Referral")
k("KPI-F03","Referral Activations","Referrals with activated_at","COUNT activated_at not null","activated_at","Referrals","Daily","Growth","Quality","Needs activation rule","Rule To Be Verified","Referral")
k("KPI-F04","Referral Conversion Rate","Converted / created","COUNT Converted / COUNT created","status","Referrals","Weekly","Growth","Programme value","Registration != conversion","Rule To Be Verified","Referral")
k("KPI-S01","Support Requests","Tickets created","COUNT ticket_id","ticket_id","Support_Tickets","Daily","Support","Load","Trend","Needs ticket data","Support")
k("KPI-S02","Issue Category Mix","Share of tickets per category","COUNT per category / total","issue_category","Support_Tickets","Weekly","Support/Product","Root causes","Top categories","Categories Proposed","Support")
k("KPI-S03","Help-Center Engagement","help_article_viewed per active user","COUNT / active users","article_id","Events","Weekly","Content","Content value","Context","Needs event","Support")
KPIS=K
# ---------- KPI test (J3): id, calculable?, why, additional data
KTEST=[
("KPI-U01","Yes - supplied data","registration_datetime and user_id present",""),
("KPI-U02","Yes - supplied data","user_id + event_datetime present; qualifying-event list must be agreed",""),
("KPI-U04","Partly - supplied data","session_status is always 'Completed' so crashed/abandoned sessions are invisible","Session end reason / abandoned flag"),
("KPI-E03/E04","Partly - supplied data","views and starts exist as timestamps; 'opened' stage not captured","task_opened event"),
("KPI-E05/E06/E07","Yes - supplied data","task_status and timestamps present",""),
("KPI-E02","Yes - supplied data","feature_name and user_id present in events",""),
("KPI-R01/R03/R04/R07","Yes - stand-in data only","Supplied data holds only reward_status on tasks; Rewards table is analyst-generated","Real Rewards table with reward_id, amount, unit, status"),
("KPI-R02","Yes - stand-in data only","Supplied data has no amount or unit","reward_amount, reward_unit in production"),
("KPI-W01..W04","Yes - stand-in data only","Wallet table analyst-generated; deduplication needed (6 planted duplicates detected)","Real ledger with unique transaction_id"),
("KPI-D01..D08","Yes - stand-in data only","Withdrawals analyst-generated; methods are placeholders","Real withdrawal timestamps, methods, reasons"),
("KPI-F01..F04","Yes - stand-in data only","Referrals analyst-generated; activation rule undefined","Real referrals + activation rule (A007)"),
("KPI-S01..S03","No","No support/help data supplied or generated","Support_Tickets, help_article_viewed"),
]
# ---------- Assumptions  (id, unknown, why, source checked, risk, owner, status)
ASSUME=[
("A001","Does backend currently emit task completion events?","Required for task analytics","Brief; not verified","High","Engineering","To Be Verified"),
("A002","Is a stable user_id issued at registration and never reused?","Cross-entity joins","Not verified","Critical","Engineering","To Be Verified"),
("A003","Is a session identifier generated in production?","Session analytics","Not verified","High","Engineering","To Be Verified"),
("A004","Do wallet entries carry a unique transaction_id?","Ledger deduplication","Not verified","Critical","Engineering","To Be Verified"),
("A005","Which reward units (VE, XP, Gems, Tokens, Spins) are live and how do they relate?","Per-unit reporting","Official About Us page names VEs, XP, Gems, Tokens, Spins and badges as internal units (S008); live status not stated","High","Product","Partly confirmed (names only); live status To Be Verified"),
("A006","Which withdrawal methods exist?","Method KPIs","Not verified","High","Product","To Be Verified"),
("A007","What defines 'activated' for a referred user?","Referral conversion","Not defined in brief","High","Product","To Be Verified"),
("A008","What timezone are timestamps stored in?","Daily metric boundaries","Not verified","High","Engineering","To Be Verified"),
("A009","Which features are production-ready (spin, mining, exchange, badges)?","Event scope","Brief warns not all are","High","Product","To Be Verified"),
("A010","Do third-party partners return completion/failure status?","Failure attribution","Not verified","High","Engineering","To Be Verified"),
("A011","Are event retries idempotent?","Duplicate events","10 duplicate event_ids in audit sheet","High","Engineering","To Be Verified"),
("A012","Is consent captured per user and stored?","Governance","consent_status in simulated users only","High","Legal/Product","To Be Verified"),
("A013","Why do Task 01 and Task 02 files give different attributes for the same user_ids?","Joins across files unsafe","Compared files directly","Medium","Data","Open - treated as independent simulations"),
("A014","Are the original Rewards/Wallet/Withdrawals/Referrals sample sheets available in the brief's Drive folder?","Stand-in data must be replaced, not mixed","Not in uploads","High","Task owner","To Be Verified"),
("A015","Do reward, wallet and withdrawal units match (VE/XP/Gems/Tokens vs payout currency)?","Cross-unit reconciliation","Stand-in data assumes VE","High","Product","To Be Verified"),
]
# ---------- Backlog (priority, requirement, reason, dependency, owner, stage)
BACK=[
("Critical","Stable user_id","Required for cross-event analysis","Authentication","Engineering","Prelaunch"),
("Critical","Unique immutable transaction_id on wallet entries","Wallet deduplication and reconciliation","Wallet service","Engineering","Prelaunch"),
("Critical","withdrawal_id and timestamped status transitions","Processing time and queue KPIs impossible without them","Withdrawal service","Engineering","Prelaunch"),
("Critical","Reward record with amount, unit, status, source link","Separate activity from credited value","Reward service","Engineering","Prelaunch"),
("Critical","Event_id idempotency key on every event","Duplicates seen in audit data","Event SDK","Engineering","Prelaunch"),
("High","Task funnel events (viewed/opened/started/completed/failed)","Completion funnel","Frontend/backend","Engineering","Prelaunch"),
("High","Controlled vocabularies (feature_name, status, reason)","Casing and spacing issues seen","Schema registry/doc","Data/Engineering","Prelaunch"),
("High","Ingestion validation (required, types, ISO-8601 UTC)","Malformed dates seen","Pipeline","Data/Engineering","Prelaunch"),
("High","Referral activation rule definition","Conversion cannot be computed","Product decision","Product","Prelaunch"),
("High","Remove direct personal fields from analytics layer","Data minimisation","Governance","Data/Legal","Prelaunch"),
("High","Provide missing Rewards/Wallet/Withdrawals/Referrals sample data","Test money KPIs","Task owner","Product","Prelaunch"),
("Medium","Partner status capture on third-party tasks","Failure attribution","Partner integrations","Engineering","Prelaunch"),
("Medium","Session end reason and abandoned status","Session health","Frontend","Engineering","Postlaunch"),
("Medium","Metric/event change log in repo","Change management","Process","Data","Prelaunch"),
("Medium","Executive and Withdrawal dashboards","Management reporting","Production data","Analytics","Postlaunch"),
("Low","Support/help-center events","Support KPIs","Support tool","Product","Postlaunch"),
]

# ---------- KPI testability per KPI (single source of truth)
_sup="U01 U02 U03 U06 U07 U08 E01 E02 E03 E04 E05 E06 E07 E08 E10 E11 E12".split()
_par="U04 U05 E09 F01".split()
_sub="R01 R02 R03 R04 R05 R06 R07 W01 W02 W03 W04 D01 D02 D03 D04 D05 D06 D07 D08 F02 F03 F04".split()
_nod="S01 S02 S03".split()
TESTCLASS={}
for g,c in ((_sup,'Supplied data'),(_par,'Partly supplied'),(_sub,'Stand-in data only'),(_nod,'No data')):
    for x in g: TESTCLASS['KPI-'+x]=c
TESTWHY={
'KPI-U04':("Sessions exist but session_status is always 'Completed', so unfinished sessions are invisible","Session end reason / abandoned flag"),
'KPI-U05':("Users has onboarding_status only; no onboarding_started/completed events or timestamps","onboarding events with timestamps"),
'KPI-E09':("streak_claimed and streak_broken events exist but no streak_count value","streak_count on streak_updated"),
'KPI-F01':("referral_created events exist but no referral_id, referred user or status","Referrals table"),
'KPI-R01':("Tasks carry no reward amount, unit or reward_id; Rewards table is analyst-generated","Real Rewards table"),
'KPI-R02':("No reward amount or unit in supplied data","reward_amount, reward_unit in production"),
}
def kpi_test_rows():
    out=[]
    for k in KPIS:
        c=TESTCLASS[k[0]]; g=k[12]
        if k[0] in TESTWHY: why,add=TESTWHY[k[0]]
        elif c=='Supplied data': why,add="Required fields exist in the supplied simulated files",""
        elif c=='Stand-in data only': why,add="Source table not supplied; formula tested on analyst-generated stand-in","Real "+k[5]+" table"
        else: why,add="No support or help data supplied or generated","Support tickets / help-article events"
        out.append((k[0],k[1],c,why,add))
    return out

set verify off
set pagesize 0
set serveroutput on size unlim
set feedback off
set define on
set sqlblanklines on
commit;
select 'Time start '||TO_CHAR(SYSDATE,  'DD/mm/YYYY HH24:MI:SS')||'  ' from dual;
set feedback on
prompt .       .       .       .       .       .       .       .       . Start: &1  Rev. &4
@&1
show errors
set define on
prompt .       .       .       .       .       .       .       .       .   End: &1
set feedback off
set feedback on
commit;
select 'Time end '||TO_CHAR(SYSDATE,  'DD/mm/YYYY HH24:MI:SS')||'  ' from dual;

select sch.OWNER, NVL(a.cnt,0) cnt
from ( select  OWNER, COUNT(*) AS CNT
from all_objects where 
status = 'INVALID' AND 
OWNER IN ('BBR','FACT','NAQ','OD','AFW$','DHW$','IMP$')
GROUP BY OWNER) a, ( select 'BBR' as OWNER from dual
union  select 'FACT' as OWNER from dual
union  select 'DHW$' as OWNER from dual
union  select 'IMP$' as OWNER from dual
union  select 'NAQ' as OWNER from dual
union  select 'AFW$' as OWNER from dual
union  select 'OD' as OWNER from dual) sch
where A.OWNER (+) = sch.owner and cnt <> 0 ORDER BY 1
/
prompt  
prompt  
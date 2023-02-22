spool d:\svn\_log_\5.06.2988.001\5.06.2988.001_ina02.log append
set serveroutput on size unlim 
set verify off
set pagesize 0
set feedback off
set define on
set sqlblanklines on

prompt;
prompt ====INVALID OBJECTS ina02==== First 50 names;
prompt;
select sch.OWNER, NVL(a.cnt,0) cnt
from ( select  OWNER, object_name AS CNT
from all_objects where 
status = 'INVALID' AND 
OWNER IN ('BBR','FACT','NAQ','OD','AFW$','DHW$','IMP$')) a, 
( select 'BBR' as OWNER from dual
union  select 'FACT' as OWNER from dual
union  select 'DHW$' as OWNER from dual
union  select 'IMP$' as OWNER from dual
union  select 'NAQ' as OWNER from dual
union  select 'AFW$' as OWNER from dual
union  select 'OD' as OWNER from dual) sch
where A.OWNER (+) = sch.owner
and rownum <= 50 
/

prompt
select 'DATE COMPILATION: ', SYSTIMESTAMP 
from dual;

spool off
exit;
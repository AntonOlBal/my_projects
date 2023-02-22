spool d:\svn\_log_\5.06.2988.001\5.06.2988.001_ina02.log
set serveroutput on 


whenever sqlerror continue
prompt ��������� ��������  DDL � DisableSpravSync
begin
registry.SetValue('PSB\COMMON\DDL_TRIGGER', null, '0');
commit;
end;
/
begin
registry.SetValue('\PSB\MDM\DisableSpravSync', null, '1');
commit;
end;
/

begin
execute immediate 'alter session set plsql_debug=false plsql_optimize_level=2';
end;
/

declare
v_cnt number;
begin
select count(*) into v_cnt from scriptpatch where SCRIPTNAME = 'psb_ver';
if v_cnt = 0 then
insert into scriptpatch (SCRIPTNAME, PATCHNAME, PATCHDATE) values ('psb_ver', '0', sysdate);
commit;
end if;
insert into scriptpatch (SCRIPTNAME, PATCHNAME, PATCHDATE) values ('psb_ver', '5.06.2988.001', sysdate);
commit;
end;
/

prompt ��������, ���� ��������
set serveroutput on
declare
name varchar2(14);
begin
select name into name from v$database ;
case 
      when  name in ('TSE15','TSF16') then dbms_output.put_line('�� ������������� ���: '||name);
      else od.psb_cp_cashpooling.OnLineCP_StopDequeue;
     end case;
end;
/

--exec psb_cross_pkg.setPatchBank
alter trigger T_tableauditlog enable;
commit;

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

prompt ����connect  ===== ������  NA-78143; === ���� ina02;;
connect SCHEMA_NAME/PASS@BASE
alter session set ddl_lock_timeout=150; 
--exec od.psb_cross_pkg.setPatchBank
begin
execute immediate 'alter session set plsql_debug=false plsql_optimize_level=2';
end;
/
@comp d:\svn\ABS\tags\5.06.2988.001\od\procedure\psb_msfo_mdf_checkevent.sql NA-78143 avvakumovsyu_1 700342;

prompt ===== ������  NA-81355; ===== ���� ina02;
@comp d:\svn\ABS\tags\5.06.2988.001\od\procedure\dpc_psb_set_indproc.sql NA-81355 avvakumovsyu_1 702428;

prompt ===== ������  NA-81355; ===== ���� ina02;
@comp d:\svn\ABS\tags\5.06.2988.001\od\procedure\psb_msfo_mdf_checkevent.sql NA-81355 avvakumovsyu_1 700347;

prompt ===== ������  NA-81355; ===== ���� ina02;
@comp d:\svn\ABS\tags\5.06.2988.001\od\trigger\psb_computerate_aiud.sql NA-81355 kacharginai 699890;

prompt ===== ������  NA-71576; ===== ���� ina02;
@comp d:\svn\ABS\tags\5.06.2988.001\od\excelrep\report_0_������_��_�������_�_������������_�_���_�������������.sql NA-71576 gulyaevmo 703649;

prompt ===== ������  NA-82241; ===== ���� ina02;
@comp d:\svn\ABS\tags\5.06.2988.001\od\excelrep\report_0_��������_���������_�_��������_�_�������_�����������.sql NA-82241 gulyaevmo 703647;

prompt ===== ������  NA-83010; ===== ���� ina02;
@comp d:\svn\ABS\tags\5.06.2988.001\od\script_dml\na_83010_add_param.sql NA-83010 sedletskiyav 703433;

prompt ===== ������  NA-83010; ===== ���� ina02;
@comp d:\svn\ABS\tags\5.06.2988.001\od\procedure\loanutil_recalcforecast.sql NA-83010 sedletskiyav 703547;
connect SCHEMA_NAME/PASS@BASE
exec psb_cross_pkg.resetPatchFlag
-------




alter trigger T_tableauditlog disable;
/

prompt ��������� �������� �������� ��������� DDL
begin
registry.SetValue('PSB\COMMON\DDL_TRIGGER', null, '1');
commit;
end;
/
begin
registry.SetValue('\PSB\MDM\DisableSpravSync', null, '0');
commit;
end;
/



prompt ��������, ����� ��������
set serveroutput on
declare
name varchar2(14);
begin
select name into name from v$database ;
case 
      when  name in ('TSE15','TSF16') then dbms_output.put_line('�� ������������� ���: '||name);
      else od.psb_cp_cashpooling.OnLineCP_StartDequeue;
     end case;
end;
/





spool off
exit;

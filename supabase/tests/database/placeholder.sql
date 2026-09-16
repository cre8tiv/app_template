begin;
select plan(1);

select ok(true, 'placeholder pgTAP test — replace once schema/RLS tests exist');

select * from finish();
rollback;

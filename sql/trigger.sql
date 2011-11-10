set term !! ;

create trigger css_autoincrement for css
active before insert position 0
as
declare variable tmp decimal(18,0);
begin
  if (new.css_id is null) then
    new.css_id = gen_id(css_gen, 1);
  else
  begin
    tmp = gen_id(css_gen, 0);
    if (tmp < new.css_id) then
      tmp = gen_id(css_gen, new.css_id-tmp);
  end
end!!

set term ; !!

SET TERM ^ ;
CREATE TRIGGER OPE_AUTOINCREMENT FOR OPERATIONS ACTIVE
BEFORE INSERT POSITION 0
AS
DECLARE VARIABLE tmp DECIMAL(18,0);
BEGIN
  IF (NEW.OPE_ID IS NULL) THEN
    NEW.OPE_ID = GEN_ID(OPE_GEN, 1);
  ELSE
  BEGIN
    tmp = GEN_ID(OPE_GEN, 0);
    if (tmp < new.OPE_ID) then
      tmp = GEN_ID(OPE_GEN, new.OPE_ID-tmp);
  END
END^
SET TERM ; ^

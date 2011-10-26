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
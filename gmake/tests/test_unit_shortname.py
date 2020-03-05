from gmake.utils import unit_shortname
from gmake.utils import human_to_string


import astropy.units as u

unit=u.Unit('Jy km /s ')
q=2*unit

print(unit_shortname(unit,nospace=True))
print(unit_shortname(unit,nospace=False))
print(unit_shortname(unit,nospace=False,options=True))

print(human_to_string(q,format_string='{0.value:0.2f} {0.unit:shortname}',nospace=False))
print(human_to_string(q,format_string='{0.value:0.2f} {0.unit:shortname}',nospace=True))
print(human_to_string(q,format_string='{0.value:0.2f} in {0.unit:shortname}',nospace=True))
print(human_to_string(q,format_string='{0.value:0.2f} in {0.unit:cds}',nospace=True))
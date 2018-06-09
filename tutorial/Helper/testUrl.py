#coding:utf-8
import urllib
import json

base  = '{"title":{"text":"","style":"font-size:15px;color:black;"},"bg_colour":"#FFFFFF","is_decimal_separator_comma":0,"elements":[{"text":"2系旅行车","animate":true,"values":[{"value":12709,"label":"宝马 5系","highlight":"alpha"},{"value":11271,"label":"宝马 3系","highlight":"alpha"},{"value":8415,"label":"宝马 X1","highlight":"alpha"},{"value":3258,"label":"宝马 1系三厢","highlight":"alpha"},{"value":580,"label":"宝马 2系旅行车","highlight":"alpha"}],"font-size":15,"radius":100,"type":"pie","start-angle":80,"tip":"占#percent#","colours":["0xcc9966","0x339933","0x3366ff","0xcc3333","0xff6600","0x996699","0xAAAA77"]}],"num_decimals":2,"is_fixed_num_decimals_forced":0,"is_thousand_separator_disabled":0}'
base = json.loads(base)
for b in base:
    print(b)
    print(base[b])
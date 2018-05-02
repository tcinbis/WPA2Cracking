# CPU tests
./hashcat64.exe -a 3 -D 1 --force -m 2500 output.hccapx ?d?d?d?d?d?d?d?d # 8 digits only --> 6h 55min
./hashcat64.exe -a 3 -D 1 --force -m 2500 output.hccapx ?l?l?l?l?l?l?l?l # 8 lower case letters only --> 1y 234d
./hashcat64.exe -a 3 -D 1 --force -m 2500 output.hccapx ?u?u?u?u?u?u?u?u # 8 upper case letters only --> 1y 220d
./hashcat64.exe -a 3 -D 1 --force -m 2500 output.hccapx ?a?a?a?a?a?a?a?a # 8 mixed characters --> NEXT BIG BAND (>10y)

# GPU tests
./hashcat64.exe -a 3 -D 2 -m 2500 output.hccapx ?d?d?d?d?d?d?d?d # 8 digits only
./hashcat64.exe -a 3 -D 2 -m 2500 output.hccapx ?l?l?l?l?l?l?l?l # 8 lower case letters only
./hashcat64.exe -a 3 -D 2 -m 2500 output.hccapx ?u?u?u?u?u?u?u?u # 8 upper case letters only
./hashcat64.exe -a 3 -D 2 -m 2500 output.hccapx ?a?a?a?a?a?a?a?a # 8 mixed characters

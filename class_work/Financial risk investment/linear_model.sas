/*�������ݼ�*/
options validvarname=any; 
proc import datafile = "C:\Users\HuZheHui\Desktop\new_house1.xls" dbms = excel out = myfile;
sheet = "sheet1";
getnames = yes;
run;

/*���ݿ��Ӻ�*/
proc univariate data=myfile;
 histogram price
run;


/*��Ԫ���Իع�*/
proc reg data=myfile;
model price=size floor subway_distance attention visit rooms decorate school/ selection=stepwise;
run;
quit;


/*��ӡ����*/
proc print data = myfile;
run;



/*创建数据集*/
options validvarname=any; 
proc import datafile = "C:\Users\HuZheHui\Desktop\new_house1.xls" dbms = excel out = myfile;
sheet = "sheet1";
getnames = yes;
run;

/*数据可视乎*/
proc univariate data=myfile;
 histogram price
run;


/*多元线性回归*/
proc reg data=myfile;
model price=size floor subway_distance attention visit rooms decorate school/ selection=stepwise;
run;
quit;


/*打印数据*/
proc print data = myfile;
run;



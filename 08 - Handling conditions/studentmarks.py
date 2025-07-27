decidingmarks=60
st_marks = int(input('Enter the student marks: '))
##85
##if marks is in between 70 to 80 u need to excellent
if st_marks>= 70 and st_marks < 80:
    print('Student has scored excellent marks')
elif st_marks>= 60 and st_marks < 70:
    print('Student has scored good marks')
elif st_marks>= 60 or st_marks > 70:
    print('Student has scored good marks')
else:
    print('Student has failed')    
if st_marks>= decidingmarks:
    print('Student has passed')
    print('Congratulations!')
else:
    print('Student has failed')
    
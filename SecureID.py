import random

import datetime
from email.mime.text import MIMEText

from flask import Flask, render_template,request,jsonify,session
from connection import conn

app = Flask(__name__)

app.secret_key="hh"

static_path="D:\\Aproject\\NEWS PORTAL\\Web\\SecureID\\SecureID\\static\\"


@app.route('/')
def login():
    return render_template("login.html")
@app.route('/log',methods=['post'])
def admin_login():
    session["logout"] = "1"
    if session["logout"] == "1":
        user=request.form['txt_uname']
        pas=request.form['txt_pasw']
        c = conn()
        de="select * from login where username='"+user+"' and password='"+pas+"'"
        d=c.selectone(de)

        if d is not None:
            if (d[3] == "admin"):
                return home()
            elif (d[3] == "college"):
                session["clg_id"] = str(d[0])
                return home()
            elif (d[3] == "staff"):
                session["stf_id"] = str(d[0])
                return home()
            elif (d[3] == "placement"):
                session["pla_id"] = str(d[0])
                return home()
            elif (d[3] == "student"):
                session["std_id"] = str(d[0])
                return home()
            elif (d[3] == "company"):
                session["cmp_id"] = str(d[0])
                return home()
            elif (d[3] == "ceo"):
                session["ce_id"] = str(d[0])
                return home()
        else:
            return "<script> alert('Invalid username or password');window.location='/' </script>"

    else:
        return "<script> alert('Invalid username or password');window.location='/' </script>"


@app.route('/home')
def home():
    if session["logout"] == "1":
        return render_template("admin/admin_home.html")
    else:
        return login()

@app.route('/college_studymaterialsupload')
def college_studymaterialsupload():
    qry="SELECT * FROM `course`"
    d=conn()
    res=d.selectall(qry)
    return render_template('/College/college_uploadmaterials.html',crs=res)



@app.route('/call_internal')
def call_internal():
    if session["logout"]=="1":
        db=conn()
        cg=db.selectall('select * from college')
        return render_template("admin/adm_call_internal.html", data=cg)
    else:
        return login()

@app.route("/adm_ajax_course_call_internal",methods=['post'])
def call_adm_ajax_course_call_internalintern():
    ci=conn()
    clg=request.form['clgid']
    dep=request.form['dptid']
    session['dep']=dep
    session['clg']=clg
    de="select course.c_id,course.c_name from course inner join course_allocation on course.c_id=course_allocation.c_id where course.d_id='"+dep+"' and course_allocation.col_id='"+clg+"'"
    res=ci.jsonsel(de)
    return jsonify(res)

@app.route("/adm_ajax_studdd",methods=['post'])
def adm_ajax_studdd():
    ci=conn()
    clg=session['clg']
    dep=session['dep']
    cou=request.form['cou']
    de="select student.*,department.d_name,course.c_name,college.col_name from student,college,course,department where student.col_id=college.login_id and student.c_id=course.c_id and student.d_id=department.d_id and student.col_id='"+clg+"' and student.c_id='"+cou+"' and student.d_id='"+dep+"' and student.sem='6'"
    res=ci.jsonsel(de)
    return jsonify(res)

@app.route("/adm_call_internal",methods=['post'])
def call_intern():
    ci=conn()
    clg=request.form['clg']
    dep=request.form['dpt']
    cou=request.form['cou']
    yr=request.form['yr']
    sem=request.form['sem']
    ka="insert into internal_requests values(null,'"+clg+"','"+dep+"','"+cou+"','"+sem+"','Pending',CURDATE(),'"+yr+"')"
    ci.nonreturn(ka)
    return render_template("admin/admin_home.html")

@app.route('/adm_view_internal')
def adm_view_internal():
    if session["logout"] == "1":
        db=conn()
        cg=db.selectall('select * from college')
        return render_template("admin/adm_view_internal.html",data=cg)
    else:
        return login()

@app.route("/adm_ajax_course_view_internal",methods=['post'])
def call_adm_ajax_course_view_internal():
    ci=conn()
    clg=request.form['clgid']
    dep=request.form['dptid']
    de="select course.c_id,course.c_name from course inner join course_allocation on course.c_id=course_allocation.c_id where course.d_id='"+dep+"' and course_allocation.col_id='"+clg+"'"
    res=ci.jsonsel(de)
    return jsonify(res)

@app.route('/adm_internal',methods=['post'])
def adm_internal():
    clg=request.form['clg']
    dep=request.form['dpt']
    cou=request.form['cou']
    sem=request.form['sem']
    session['sem']=sem
    se="select student.*,department.d_name,college.col_name from college,department,student where college.login_id=student.col_id and student.d_id=department.d_id and student.col_id='"+clg+"' and student.d_id='"+dep+"' and student.sem='"+sem+"'"
    c=conn()
    re=c.selectall(se)
    cg = c.selectall('select * from college')
    return  render_template("admin/adm_view_internal.html",data=cg,data2=re)


@app.route('/adm_view_inte/<stid>')
def adm_view_inte(stid):
    if session["logout"] == "1":
        qry="select subject.sub_code,subject.sub,internal.internals from internal,subject where internal.sub_id=subject.sub_id and subject.sem='"+str(session['sem'])+"' and internal.s_id='"+str(session['st_id'])+"'"
        c=conn()
        re=c.selectall(qry)
        return render_template("admin/adm_view_internal2.html",data=re)
    else:
        return login()

@app.route("/adm_sub_by_sem",methods=['post'])
def call_adm_course_view_internal():
    ci=conn()
    sem=request.form['sem']
    cou=request.form['cou']
    de="select sub_id,sub from subject where c_id='"+cou+"' and sem='"+sem+"'"
    res=ci.jsonsel(de)
    return jsonify(res)


@app.route('/view_cmplaint')
def view_complaint():
    if session["logout"] == "1":
        c = conn()
        co="select student.s_name,complaint.cmplaint,complaint.status,complaint.date,complaint.cm_id,complaint.reply from complaint,student where student.login_id=complaint.s_id and complaint.reply='pending'"
        cm=c.selectall(co)
        return render_template("admin/adm_view_complaint.html",data=cm)
    else:
        return login()


@app.route('/reply/<id>')
def reply(id):
    if session["logout"] == "1":
        c = conn()
        de="select * from complaint where cm_id='"+id+"'"
        ce=c.selectone(de)
        return render_template("admin/adm_comp_reply.html",data=ce)
    else:
        return login()

@app.route('/comp_reply',methods=['post'])
def comp_reply():
    c = conn()
    com=request.form['cm_id']
    rep=request.form['reply']
    up="update complaint set reply='"+rep+"',status='replied' where cm_id='"+com+"'"
    c.nonreturn(up)
    return view_complaint()


@app.route('/adm_certificate')
def adm_certificate():
    if session["logout"] == "1":
        db=conn()
        cg=db.selectall('select * from college')
        return render_template("admin/certificate_generatn.html",data=cg)
    else:
        return login()


@app.route("/adm_cert_gen/<stid>")
def adm_cert_gen(stid):
    r1=random.randint(00,99)
    r2=random.randint(00,99)
    r3 = random.randint(00, 99)
    r4 = random.randint(00, 99)
    s=str(r1)+"#"+str(r2)+"#"+str(stid)+"#"+str(r3)+"#"+str(r4)+"#"

    c=conn()
    import pyqrcode
    # Generate QR code
    url = pyqrcode.create(s)
    # Create and save the png file naming "myqr.png"
    url.svg(static_path+"qr\\"+stid+".svg", scale=8)

    qry="select department.d_name,student.s_name,course.c_name from department,course,student where student.c_id=course.c_id and student.d_id=department.d_id and student.login_id='"+stid+"'"
    res=c.selectone(qry)
    qr_path="/static/qr/"+stid+".svg"
    return render_template("admin/adm_cert.html",res=res,data2=qr_path)


@app.route('/course')
def cou_alloc():
    if session["logout"] == "1":
        dc=conn()
        cg=dc.selectall('select * from college')
        co=dc.selectall('select * from course')
        return render_template("admin/adm_cou_alloc.html",data=cg,data2=co)
    else:
        return login()

@app.route('/course_by_clg',methods=['post'])
def course_by_clg():
    c = conn()
    clg = request.form['clg']
    session['col_id'] = clg
    zz = "select * from course where c_id not in(select c_id from course_allocation where col_id='"+clg+"')"
    res = c.jsonsel(zz)
    return jsonify(res)


@app.route("/adm_cou_alloc",methods=['post'])
def cou_allo():
    ca=conn()
    clg=request.form['clg']
    cou=request.form['cou']
    qry="SELECT * FROM course_allocation WHERE col_id='"+clg+"' AND c_id='"+cou+"'"
    res=ca.selectone(qry)
    if res is not None:
        return "<script>alert('Course Already exists');window.location='/course'</script>"
    else:
        a="insert into course_allocation values(null,'"+clg+"','"+cou+"')"
        ca.nonreturn(a)
        return "<script>alert('Course Allocated');window.location='/course';</script>"

@app.route('/view_coualc')
def view_coual():
    if session["logout"] == "1":
        c=conn()
        co="select college.col_name,course.c_name,course_allocation.col_id,course_allocation.ca_id from course,college,course_allocation where college.login_id=course_allocation.col_id and course.c_id=course_allocation.c_id"
        cu=c.selectall(co)
        return render_template("admin/adm_view_coualc.html",data=cu)
    else:
        return login()


@app.route('/search_course',methods=['post'])
def search_course():
    if session["logout"] == "1":
        c=conn()
        txt=request.form['ser']
        co="select college.col_name,course.c_name,course_allocation.col_id,course_allocation.ca_id from course,college,course_allocation where college.login_id=course_allocation.col_id and course.c_id=course_allocation.c_id and college.col_name like '%"+txt+"%' "
        cu = c.selectall(co)
        return render_template("admin/adm_view_coualc.html", data=cu)
    else:
        return login()


@app.route('/delete_coualc/<id>')
def del_coualc(id):
    c = conn()
    de="delete from course_allocation where course_allocation.ca_id='"+id+"'"
    c.nonreturn(de)
    return view_coual()


@app.route('/cou_mgm')
def cou_manage():
    if session["logout"] == "1":
        db=conn()
        qry=db.selectall("select * from department")
        return render_template("admin/adm_cou_mngmnt.html",data=qry)
    else:
        return login()


@app.route("/adm_cou_mngmnt",methods=['post'])
def adm_cou_mngmnt_post():
    ca=conn()
    cou=request.form['couname']
    cid=request.form['dpt']
    co="insert into course values (null,'"+cid+"','"+cou+"')"
    ca.nonreturn(co)
    return "<script>alert('Course Added');window.location='/cou_mgm';</script>"

@app.route('/dpt_mgm')
def dpt_manage():
    if session["logout"] == "1":
        return render_template("admin/adm_dpt_mngmnt.html")
    else:
        return login()


@app.route("/adm_dep_mgmt_post",methods=['post'])
def adm_dep_mgmt_post():
    c = conn()
    dep=request.form['dptname']
    q="insert into department(d_name) values('"+dep+"')"
    c.nonreturn(q)
    return "<script>alert('Department Added');window.location='/dpt_mgm';</script>"

@app.route('/view_dpt')
def view_dpt():
    if session["logout"] == "1":
        c = conn()
        q="select * from department"
        r=c.selectall(q)
        return render_template("admin/adm_view_dpt.html",data=r)
    else:
        return login()






@app.route("/serch_dpt",methods=['post'])
def serch_dpt():
        c = conn()
        names=request.form['ser']
        q="SELECT * FROM `department` WHERE `d_name` LIKE'"+names+"%'"
        r=c.selectall(q)
        return render_template("admin/adm_view_dpt.html",data=r)
   




@app.route('/edit_cou/<id>')
def edit_cou(id):
    c = conn()
    d="select * from department"
    r=c.selectall(d)
    qr="select course.c_id,course.c_name,department.d_id,department.d_name from course,department where course.d_id=department.d_id and course.c_id='"+id+"'"
    dd = c.selectone(qr)
    return render_template("admin/adm_edit_cou.html",data=r,data2=dd)

@app.route('/update_cou',methods=['post'])
def update_cou():
    db=conn()
    dpt=request.form['dpt']
    cou=request.form['couname']
    cid=request.form['cid']
    re="update course set d_id='"+dpt+"',c_name='"+cou+"' where c_id='"+cid+"'"
    db.nonreturn(re)
    return view_cou()

@app.route('/delete_cou/<id>')
def delete_cou(id):
    de="delete from course where c_id='"+id+"'"
    c = conn()
    c.nonreturn(de)
    return view_cou()


@app.route('/edit_dpt/<id>')
def edit_dep(id):
    c = conn()
    q="select * from department where d_id='"+id+"'"
    r=c.selectone(q)
    return render_template("admin/adm_edit_dpt.html",data=r)

@app.route('/update_dpt',methods=['post'])
def update_dpt():
    db=conn()
    dpt=request.form['dptname']
    did=request.form['did']
    d="update department set d_name='"+dpt+"' where d_id='"+did+"'"
    db.nonreturn(d)
    return view_dpt()

@app.route('/delete_dpt/<id>')
def delete_dpt(id):
    d="delete from department where d_id='"+id+"'"
    c = conn()
    c.nonreturn(d)
    return view_dpt()


@app.route('/sub_alloc')
def sub_alloc():
    db=conn()
    q=db.selectall("select * from course")
    v=db.selectall("select * from subject")
    return render_template("admin/adm_sub_alloc.html",data=q,data2=v)
@app.route("/adm_sub_alloc",methods=['post'])
def adm_sub_alloc():
    ca=conn()
    cou=request.form['cou']
    sub=request.form['sub']
    se=request.form['sem']
    al="insert into subject_allocation(subal_id,c_id,sub_id,sem) values (null,'"+cou+"','"+sub+"','"+se+"')"
    ca.nonreturn(al)
    return render_template("admin/admin_home.html")

@app.route('/view_suballo')
def view_suballo():
    c=conn()
    zz="select course.c_name,subject.sub,subject_allocation.sem,subject_allocation.c_id,subject_allocation.subal_id from course,subject,subject_allocation where subject.sub_id=subject_allocation.sub_id and subject_allocation.c_id=course.c_id"
    so=c.selectall(zz)
    return render_template("admin/adm_view_suballoc.html",data=so)


@app.route('/edit_suballoc/<id>')
def edit_suballoc(id):
    c = conn()
    co="select course.c_name,subject.sub,subject_allocation.sem,subject_allocation.c_id,subject_allocation.subal_id,subject_allocation.sub_id,course.c_id from course,subject_allocation,subject where subject_allocation.sub_id=subject.sub_id and course.c_id=subject_allocation.c_id and subject_allocation.subal_id='"+id+"'"
    ce=c.selectone(co)
    su="select * from course"
    se=c.selectall(su)
    co="select * from subject"
    co=c.selectall(co)
    return render_template("admin/adm_edit_suballoc.html",data=ce,data2=se,data3=co)


@app.route('/update_suballoc',methods=['post'])
def update_suballoc():
    cu=request.form['cou']
    si=request.form['sub']
    se=request.form['sem']
    subalid=request.form['subalid']
    c = conn()
    de="update subject_allocation set c_id='"+cu+"',sub_id='"+si+"',sem='"+se+"' where subal_id='"+subalid+"'"
    c.nonreturn(de)
    return view_suballo()

@app.route('/delete_suballoc/<id>')
def del_suballo(id):
    c = conn()
    de="delete from subject_allocation where subject_allocation.subal_id='"+id+"'"
    c.nonreturn(de)
    return view_suballo()


@app.route('/sub_mgmt')
def sub_mgmt():
    if session["logout"] == "1":
        db=conn()
        qry=db.selectall("select * from course")
        return render_template("admin/adm_sub_mngmnt.html",data=qry)
    else:
        return login()

@app.route("/adm_sub_mngmnt",methods=['post'])
def adm_sub_mngmnt_post():
    ca=conn()
    sub=request.form['subname']
    sid=request.form['subcode']
    cu=request.form['cou']
    sem=request.form['sem']
    co="insert into subject values (null,'"+cu+"','"+sub+"','"+sid+"','"+sem+"')"
    ca.nonreturn(co)
    return "<script>alert('Subject Added');window.location='/sub_mgmt';</script>"

@app.route('/view_clg')
def view_clg():
    if session["logout"] == "1":
        c = conn()
        bb="select * from college,login where college.login_id=login.login_id"
        r=c.selectall(bb)
        return render_template("admin/adm_view_college.html",data=r)
    else:
        return login()

@app.route('/publicview_clg')
def publicview_clg():
    if "1" == "1":
        c = conn()
        bb="select * from college,login where college.login_id=login.login_id"
        r=c.selectall(bb)
        return render_template("pub_home.html",data=r)
    else:
        return login()

@app.route('/view_clg_post',methods=['post'])
def view_clg_post():

    name=request.form['name']

    if session["logout"] == "1":
        c = conn()
        bb="select * from college,login where college.login_id=login.login_id and col_name like '%"+name+"%'"
        r=c.selectall(bb)
        return render_template("admin/adm_view_college.html",data=r)
    else:
        return login()


@app.route('/viewmore_clg/<logid>')
def viewmore_clg(logid):
    c = conn()
    bb = "select * from college,login where college.login_id=login.login_id and login.login_id='"+logid+"' "
    r = c.selectone(bb)
    return render_template("admin/adm_viwmore_college.html", data=r)

@app.route('/pubviewmore_clg/<logid>')
def pubviewmore_clg(logid):
    c = conn()
    bb = "select * from college,login where college.login_id=login.login_id and login.login_id='"+logid+"' "
    r = c.selectone(bb)
    bb = "SELECT `course`.* FROM `course_allocation`,`course` WHERE `course_allocation`.`c_id`=`course`.`c_id` AND `course_allocation`.`col_id`='"+logid+"' "
    res = c.selectall(bb)
    return render_template("pub_viwmore_college.html", data=r,data2=res)


@app.route("/adm_acc_rej_clg",methods=['post'])
def adm_acc_rej_clg():
    logid=request.form['logid']
    btn=request.form['btn']
    c = conn()
    if btn=='ACCEPT':
        qry="update login set type='college' where login_id='"+logid+"'"
        c.nonreturn(qry)
        return "<script>alert('Accepted');window.location='/view_clg';</script>"
    elif btn=='REJECT':
        qry = "update login set type='reject' where login_id='" + logid + "'"
        c.nonreturn(qry)
        return "<script>alert('Rejected');window.location='/view_clg';</script>"




@app.route('/view_cou')
def view_cou():
    if session["logout"] == "1":
        c = conn()
        c1="SELECT * FROM department"
        res=c.selectall(c1)
        cc='select department.d_name,course.* from course,department where department.d_id=course.d_id'
        ca=c.selectall(cc)
        return render_template("admin/adm_view_cou.html",data=ca,data2=res)
    else:
        return login()


@app.route('/dept_wise',methods=['post'])
def dept_wise():
        c = conn()
        c1="SELECT * FROM department"
        res=c.selectall(c1)
        names=request.form['select']
        cc="select department.d_name,course.* from course,department where department.d_id=course.d_id AND department.d_id='"+names+"'"
        ca=c.selectall(cc)
        return render_template("admin/adm_view_cou.html",data=ca,data2=res)
        

@app.route('/deletearticle',methods=['post'])
def deletearticle():

    aid=request.form["aid"]
    qry="delete from `article` WHERE `article_id`='"+aid+"'"
    c=conn()
    c.nonreturn(qry)
    return jsonify(status="ok")




@app.route('/view_sub')
def view_sub():
    if session["logout"] == "1":
        c = conn()
        bb="SELECT * FROM `course`"
        res1=c.selectall(bb)
        aa='select course.c_name,subject.sub,subject.sub_code,subject.sub_id,subject.sem from subject,course where course.c_id=subject.c_id'
        su=c.selectall(aa)
        return render_template("admin/adm_view_sub.html",data=su,data2=res1)
    else:
        return login()


@app.route('/view_subtsby',methods=['post'])
def view_subtsby():
        c = conn()
        name1=request.form['select1']
        name2=request.form['select2']
        bb="SELECT * FROM course"
        res1=c.selectall(bb)
        aa="select course.c_name,subject.sub,subject.sub_code,subject.sub_id,subject.sem from subject,course where course.c_id=subject.c_id AND subject.c_id='"+name1+"' AND subject.sem='"+name2+"'"
        su=c.selectall(aa)

        return render_template("admin/adm_view_sub.html",data=su,data2=res1)
          


@app.route('/edit_sub/<id>')
def edit_sub(id):
    c = conn()
    co="select * from course"
    su="select course.c_id,course.c_name,subject.sub_id,subject.sub,subject.sub_code,subject.sem from course,subject where subject.c_id=course.c_id and subject.sub_id='"+id+"'  "
    ab=c.selectall(co)
    cd=c.selectone(su)
    return render_template("admin/adm_edit_sub.html",data=ab,data2=cd)

@app.route('/update_sub',methods=['post'])
def update_sub():
    db=conn()
    cu=request.form['cou']
    su=request.form['sub']
    sc=request.form['subcode']
    subid=request.form['subid']
    sem=request.form['sem']
    re="update subject set sub='"+su+"',c_id='"+cu+"',sub_code='"+sc+"',sem='"+sem+"' where sub_id='"+subid+"'"
    db.nonreturn(re)
    return view_sub()
@app.route('/delete_sub/<id>')
def delete_sub(id):
    c = conn()
    da="delete from subject where sub_id='"+id+"'"
    c.nonreturn(da)
    return view_sub()


@app.route('/add_ext')
def add_ext():
    if session["logout"] == "1":
        db=conn()
        clg=db.selectall('select * from college')
        return render_template("admin/adm_add_ext.html",data3=clg)
    else:
        return login()

@app.route('/adm_ajax_add_ext',methods=['post'])
def adm_ajax_add_ext():
    ci=conn()
    clg=request.form['clgid']
    dep=request.form['depid']
    ce="select course.c_id,course.c_name from course inner join course_allocation on course.c_id=course_allocation.c_id where course.d_id='"+dep+"' and course_allocation.col_id='"+clg+"'"
    res=ci.jsonsel(ce)
    return jsonify(res)

@app.route('/adm_add_ext',methods=['post'])
def adm_add_ext():
    c=conn()
    clg=request.form['clg']
    dep=request.form['dept']
    cou= request.form['cou']
    sem= request.form['sem']
    session['crs_id']=cou
    session['col_id']=clg
    session['sem']=sem
    zz="select student.photo,student.s_name,course.c_name,department.d_name,college.col_name,course.c_id,student.login_id from student,course,department,college where student.col_id='"+clg+"' and student.d_id='"+dep+"' and student.c_id='"+cou+"' and student.sem='"+sem+"' and student.col_id=college.col_id and student.d_id=department.d_id and student.c_id=course.c_id"
    ex=c.selectall(zz)
    return render_template("admin/adm_add_ext.html",data4=ex)

@app.route('/ent_ext/<stid>')
def ent_ext(stid):
    if session["logout"] == "1":
        c = conn()
        session['st_id']=stid
        so="select * from subject where subject.c_id='"+str(session['crs_id'])+"'and subject.sem='"+str(session['sem'])+"' "
        se=c.selectall(so)
        return render_template("admin/adm_enter_ext.html",data=se)
    else:
        return login()
@app.route('/adm_enter_ext',methods=['post'])
def adm_enter_ext():
    ca=conn()
    sub=request.form['sub']
    mark=request.form['mark']
    qr=ca.selectone("select * from external where s_id='"+str(session['st_id'])+"' and sub_id='"+sub+"'")
    if qr is None:
        re="insert into external values(null,'"+str(session['st_id'])+"','"+sub+"','"+mark+"')"
    else:
        re = "update external set mark='" + mark + "' where extrn_id='"+str(qr[0])+"'"
    ca.nonreturn(re)
    st=session['st_id']
    return ent_ext(st)

@app.route('/clg_reg')
def clg_reg():
    return render_template("College/clg_Registration.html")


@app.route('/add_clg',methods=['post'])
def add_clg():
    c = conn()
    clg = request.form['clgname']
    ph = request.form['phnum']
    em = request.form['email']
    pl = request.form['place']
    pi = request.form['pin']
    po = request.form['post']
    pic = request.files['photo']
    district = request.form['district']
    state = request.form['state']

    qry="select * from login where username='"+em+"'"
    ress=c.selectone(qry)
    if ress is not None:
        return "<script>alert('Mail Already exists');window.location='/clg_reg'</script>"
    else:
        pic = request.files['photo']
        pic.save(static_path + "clg\\" + pic.filename)
        path = "/static/clg/" + pic.filename
        psw = random.randint(0000, 9999)
        la = "insert into login values(null,'" + em + "','" + str(psw) + "','college')"
        log = c.nonreturn(la)
        co = "insert into college values(null,'"+clg+"','"+path+"','"+ph+"','"+em+"','"+po+"','"+pi+"','"+pl+"','"+str(log)+"','"+district+"','"+state+"')"
        c.nonreturn(co)
        return "<script>alert('Successfully added'); window.location='/clg_reg'</script>"



    
@app.route('/collegedel/<cid>/<id>')
def collegedel(cid,id):
    d=conn()
    d.nonreturn("delete from login where login_id='"+id+"'")
    d.nonreturn("delete from college where col_id='"+cid+"'")

    return "<script>alert('Successfully deleted'); window.location='/view_clg'</script>"






@app.route('/clg_staff_mangmnt')
def stf_mngmnt():
    if session["logout"] == "1":
        c = conn()
        de = "select distinct(department.d_id),d_name from department,course,course_allocation where course.c_id=course_allocation.c_id and department.d_id=course.d_id and course_allocation.col_id='" + str(session['clg_id']) + "'"
        do = c.selectall(de)
        return render_template("College/clg_stfmanagement.html",data=do)
    else:
        return login()


@app.route('/clg_stf_add',methods=['post'])
def stf_manage():
    ca=conn()
    stf=request.form['stfname']
    dep=request.form['dep']
    gen=request.form['radio']
    hou=request.form['houname']
    pi=request.form['pin']
    po=request.form['post']
    ph=request.form['phnum']
    em=request.form['email']
    qu=request.form['qual']
    ex=request.form['exp']
    im=request.files['photo']

    qry="select * from login where username='"+em+"'"
    ds=ca.selectone(qry)
    if ds is not None:
        return "<script>alert('Already mail exists');window.location='/clg_staff_mangmnt'</script>"
    else:
        dd=str(datetime.datetime.now()).replace(" ","_").replace(":","_").replace("-","_")
        im.save(static_path+"staff\\"+dd+".jpg")
        path="/static/staff/"+dd+".jpg"
        pasw=str(random.randint(0000,9999))
        qr=ca.nonreturn("insert into login(username,password,type) values('"+em+"','"+pasw+"','staff')")
        fu="insert into staff values(null,'"+stf+"','"+dep+"','"+gen+"','"+hou+"','"+po+"','"+pi+"','"+ph+"','"+em+"','"+path+"','"+qu+"','"+ex+"','"+str(qr)+"','"+str(session['clg_id'])+"')"
        ca.nonreturn(fu)
        return "<script>alert('Staff Added');window.location='/clg_staff_mangmnt';</script>"


    
@app.route('/clg_view_staff')
def clg_view_staff():
    if session["logout"] == "1":
        c = conn()
        st="select staff.*,department.d_name from department,staff where staff.dep_name=department.d_id and staff.col_id='"+str(session['clg_id'])+"'"
        sa=c.selectall(st)
        return render_template("College/clg_view staff.html",data=sa)
    else:
        return login()

@app.route('/clg_view_staff_search_post',methods=['post'])
def clg_view_staff_search_post():
    name=request.form["name"]
    if session["logout"] == "1":
        c = conn()
        st="select staff.*,department.d_name from department,staff where staff.dep_name=department.d_id and staff.col_id='"+str(session['clg_id'])+"' and st_name like '%"+name+"%'"
        sa=c.selectall(st)
        return render_template("College/clg_view staff.html",data=sa)
    else:
        return login()


@app.route('/update_staff/<id>')
def update_stf(id):
    c = conn()
    st="select staff.*,department.d_name from department,staff where staff.dep_name=department.d_id and staff.staf_id='"+id+"'"
    sa=c.selectone(st)
    de = c.selectall("select distinct(department.d_id),d_name from department,course,course_allocation where course.c_id=course_allocation.c_id and department.d_id=course.d_id and course_allocation.col_id='" + str(session['clg_id']) + "'")
    return render_template("College/clg_update stf.html",data=sa,data2=de)

@app.route('/update_data',methods=['post'])
def update_data():
     ca=conn()
     sta=request.form['stfname']
     dep=request.form['dep']
     gen=request.form['radio']
     hou=request.form['houname']
     pi=request.form['pin']
     po=request.form['post']
     ph=request.form['phnum']
     qu=request.form['qual']
     ex=request.form['exp']
     stid=request.form['stfid']
     if 'photo' in request.files:
         im = request.files['photo']
         if im.filename=="":
             ab = "update staff set st_name='" + sta + "',dep_name='" + dep + "',gender='" + gen + "',h_name='" + hou + "',pin='" + pi + "',post='" + po + "',ph_no='" + ph + "',qual='" + qu + "',experience='" + ex + "' where staf_id='" + stid + "'"
         else:
             dd=str(datetime.datetime.now()).replace(" ","_").replace(":","_").replace("-","_")
             im.save(static_path+"staff\\"+dd+".jpg")
             path="/static/staff/"+dd+".jpg"
             ab="update staff set st_name='"+sta+"',dep_name='"+dep+"',gender='"+gen+"',h_name='"+hou+"',pin='"+pi+"',post='"+po+"',ph_no='"+ph+"',qual='"+qu+"',experience='"+ex+"',photo='"+path+"' where staf_id='"+stid+"'"
     else:
         ab = "update staff set st_name='" + sta + "',dep_name='" + dep + "',gender='" + gen + "',h_name='" + hou + "',pin='" + pi + "',post='" + po + "',ph_no='" + ph + "',qual='" + qu + "',experience='" + ex + "' where staf_id='" + stid + "'"
     ca.nonreturn(ab)
     return clg_view_staff()

@app.route('/delete_staff/<id>')
def delete_stf(id):
    c = conn()
    se="delete from staff where staf_id='"+id+"'"
    c.nonreturn(se)
    return clg_view_staff()


@app.route('/clg_view_cou')
def clg_view_cou():
    if session["logout"] == "1":
        c = conn()
        de="select distinct(department.d_id),d_name from department,course,course_allocation where course.c_id=course_allocation.c_id and department.d_id=course.d_id and course_allocation.col_id='"+str(session['clg_id'])+"'"
        do=c.selectall(de)
        return render_template("College/clg_View course.html",data=do)
    else:
        return login()


@app.route('/clg_cou',methods=['post'])
def clg_cou():
    c = conn()
    dept=request.form['dptname']
    cc="select course.c_id,course.c_name from course,course_allocation where course.c_id=course_allocation.c_id and course_allocation.col_id='"+session["clg_id"]+"' and course.d_id='"+dept+"'"
    ce=c.selectall(cc)
    return render_template("College/clg_View course.html",data2=ce)

@app.route('/view_subjects/<id>')
def view_subjects(id):
    c=conn()
    qry="SELECT * FROM SUBJECT WHERE c_id='"+id+"'"
    res=c.selectall(qry)
    return render_template('College/clg_sub_view.html',data=res)

@app.route('/clg_view_profile')
def clg_view_profile():
    if session["logout"] == "1":
        c = conn()
        pr="select * from college where login_id='"+session["clg_id"]+"'"
        ac=c.selectone(pr)
        return render_template("College/clg_View profile.html",i=ac)
    else:
        return login()
@app.route('/clgeditprofile')
def coledtpfl():
    c = conn()
    pr="select * from college where login_id='"+session["clg_id"]+"'"
    ac=c.selectone(pr)
    return render_template("College/clg_edit profile.html",i=ac)

@app.route('/clgupdprofile',methods=['post'])
def clgupdprofile():
    name=request.form['name']
    phone=request.form['phone']
    pin=request.form['pin']
    post=request.form['post']
    place=request.form['place']

    c=conn()
    qry="UPDATE `college` SET `col_name`='"+name+"' ,`ph_no`='"+phone+"',`post`='"+post+"',`pin`='"+pin+"',`place`='"+place+"' WHERE `login_id`='"+session["clg_id"]+"'"
    c.nonreturn(qry)

    return "<Script>alert('COllege profile updated');window.location='/clg_view_profile'</script>"






@app.route('/clg_view_request')
def clg_view_request():
    if session["logout"] == "1":
        c = conn()
        pr="select * from course"
        ac=c.selectall(pr)
        return render_template("College/clg_view_internalmark_request.html",data2=ac)
    else:
        return login()


@app.route('/clg_internal',methods=['post'])
def clg_internal():
    c = conn()
    dept=request.form['cou']
    x=session['clg_id']
    cc= "select internal_requests.*,course.c_name from internal_requests,course where course.c_id=internal_requests.crs_id and internal_requests.crs_id='"+dept+"' and internal_requests.col_id='"+str(x)+"'"
    ce=c.selectall(cc)
    return render_template("College/clg_view_internalmark_request.html",data=ce)


@app.route('/update_request/<rid>')
def update_request(rid):
    c = conn()
    ut="update internal_requests set status='confirmed' where ir_id='"+rid+"'"
    c.nonreturn(ut)
    return clg_view_request()

@app.route('/clg_student_management')
def clg_std_mng():
    if session["logout"] == "1":
        c = conn()
        co="select distinct(department.d_id),department.d_name from course_allocation,course,department where course_allocation.c_id=course.c_id and course.d_id=department.d_id and course_allocation.col_id='"+str(session['clg_id'])+"'"
        cu=c.selectall(co)
        return render_template("College/clg_student_registration.html",data=cu)
    else:
        return login()

@app.route("/clg_crs_by_dep_ajax",methods=['post'])
def clg_crs_by_dep_ajax():
    dep=request.form['dep']
    clg=str(session['clg_id'])
    qr="select distinct(course.c_name),course.c_id from course_allocation,course where course_allocation.c_id=course.c_id and course.d_id='"+dep+"' and course_allocation.col_id='"+clg+"'"
    c=conn()
    res=c.jsonsel(qr)
    return jsonify(res)


@app.route('/clg_std_reg',methods=['post'])
def std_reg():
    stf = request.form['stdname']
    did=request.form['depname']
    crs = request.form['couname']
    gen = request.form['radio']
    hou = request.form['hname']
    pi = request.form['pin']
    po = request.form['post']
    ph = request.form['phone']
    em = request.form['email']
    im = request.files['photo']
    colid=session['clg_id']
    se=request.form['sem']
    ba=request.form['batch']

    qry="select * from login where username='"+em+"'"
    c = conn()
    res1=c.selectone(qry)

    if res1 is not None:
        return "<script>alert('Account already exists');window.location='/clg_student_management'</script>"

    else:
        dd=str(datetime.datetime.now()).replace(":","_").replace(" ","_").replace("-","_")
        im.save(static_path+"stud_img\\"+dd+".jpg")
        path="/static/stud_img/"+dd+".jpg"
    
        psw=random.randint(0000,9999)
        qr="insert into login(username,password,type) values('"+em+"','"+str(psw)+"','student')"
        lid=c.nonreturn(qr)
        st="insert into student(col_id,c_id,s_name,gender,h_name,post,pin,email,photo,login_id,sem,batch,d_id,phone) values('"+str(colid)+"','"+crs+"','"+stf+"','"+gen+"','"+hou+"','"+po+"','"+pi+"','"+em+"','"+path+"','"+str(lid)+"','"+se+"','"+ba+"','"+did+"','"+ph+"')"
        c.nonreturn(st)
        return "<script>alert('Student Added');window.location='/clg_student_management';</script>"




    
@app.route('/clg_view_std')
def view_std():
    if session["logout"] == "1":
        c = conn()
        st="select * from student where col_id='"+str(session['clg_id'])+"' "
        se=c.selectall(st)
        a="select c_name from course,student where course.c_id=student.c_id"
        b=c.selectone(a)
        return render_template("College/clg_view_student.html",data=se,data2=b)
    else:
        return login()


@app.route('/edit_std/<id>')
def edit_std(id):
    c = conn()
    sa="select * from student where s_id='"+id+"'"
    si=c.selectone(sa)
    co = "select distinct(department.d_id),department.d_name from course_allocation,course,department where course_allocation.c_id=course.c_id and course.d_id=department.d_id and course_allocation.col_id='" + str(session['clg_id']) + "'"
    cu = c.selectall(co)
    return render_template("College/clg_Update_student.html",data=si,data2=cu)

@app.route('/update_std',methods=['post'])
def update_std():
    stf = request.form['stdname']
    dep = request.form['depname']
    cid=request.form['couname']
    gen = request.form['radio']
    hou = request.form['hname']
    pi = request.form['pin']
    po = request.form['post']
    ph = request.form['phone']
    se = request.form['sem']
    ba = request.form['batch']
    sid=request.form['stid']
    c = conn()
    if 'pic' in request.files:
        dd=str(datetime.datetime.now()).replace(" ","_").replace(":","_").replace("-","_")
        img=request.files['pic']
        if img.filename=="":
            a = "update student set d_id='"+dep+"',s_name='" + stf + "',c_id='" + cid + "',gender='" + gen + "',h_name='" + hou + "',pin='" + pi + "',post='" + po + "',phone='" + ph + "',sem='" + se + "',batch='" + ba + "' where s_id='" + sid + "'"
        else:
            img.save(static_path+"stud_img\\"+dd+".jpg")
            path="/static/stud_img/"+dd+".jpg"
            a="update student set d_id='"+dep+"',s_name='" + stf + "',c_id='" + cid + "',gender='"+gen+"',h_name='"+hou+"',pin='"+pi+"',post='"+po+"',phone='"+ph+"',photo='"+path+"',sem='"+se+"',batch='"+ba+"' where s_id='"+sid+"'"
    else:
        a = "update student set d_id='"+dep+"',s_name='" + stf + "',c_id='" + cid + "',gender='" + gen + "',h_name='" + hou + "',pin='" + pi + "',post='" + po + "',phone='" + ph + "',sem='" + se + "',batch='" + ba + "' where s_id='" + sid + "'"
    c.nonreturn(a)
    return view_std()

@app.route('/delete_std/<id>/<did>')
def delete_std(id,did):
    c = conn()
    ds="delete from student where s_id='"+id+"'"
    c.nonreturn(ds)
    qry="delete from login where login_id='"+did+"'"
    c.nonreturn(qry)
    return view_std()

@app.route('/placemnt_managmnt')
def placemntcell_reg():
    if session["logout"] == "1":
        return render_template("College/clg_placementcell_mangmnt.html")
    else:
        return login()


@app.route('/placement_reg',methods=['post'])
def placement_reg():
    c = conn()
    stf = request.form['hdname']
    gen = request.form['radio']
    hou = request.form['hname']
    pi = request.form['pin']
    po = request.form['post']
    ph = request.form['cont']
    em = request.form['email']
    im = request.files['photo']
    colid = session['clg_id']
    dd=str(datetime.datetime.now()).replace(" ","_").replace("-","_").replace(":","_")
    im.save(static_path+"placement_cell\\"+dd+".jpg")
    path="/static/placement_cell/"+dd+".jpg"
    psw=str(random.randint(0000,9999))
    qr=c.nonreturn("insert into login(username,password,type) values('"+em+"','"+psw+"','placement')")
    st="insert into placement values(null,'"+stf+"','"+gen+"','" + hou + "','" + po + "','" + pi + "','" + ph+ "','" + em + "','" + path + "','" + str(qr) + "','"+str(colid)+"')"
    c.nonreturn(st)
    return "<script>alert('Placement Cell Registered');window.location='/placemnt_managmnt';</script>"


@app.route('/view_placement')
def view_cell():
    if session["logout"] == "1":
        c = conn()
        sc="select * from placement where col_id='"+str(session['clg_id'])+"'"
        se=c.selectall(sc)
        return render_template("College/clg_view_placement.html",data=se)
    else:
        return login()

@app.route('/collegeviewsubjects')
def collegeviewsubjects():
    d=conn()
    qry="SELECT * FROM `course`"
    crs=d.selectall(qry)
    return render_template('/College/Collegeviewsubjects.html',crs=crs)

@app.route('/collegeviewsubjects_post',methods=['post'])
def collegeviewsubjects_post():
    d=conn()
    qry="SELECT * FROM `course`"
    crs=d.selectall(qry)
    cid=request.form['crsname']
    sem=request.form['seme']

    session["selcid"]=cid
    session["selsem"]=sem

    qry="SELECT * FROM `subject` WHERE `c_id`='"+cid+"' AND `sem`='"+sem+"'"

    res=d.selectall(qry)
    return render_template('/College/Collegeviewsubjects.html',crs=crs,ressubjects=res)

@app.route('/collegestudymaterialsload/<subid>')
def collegestudymaterialsload(subid):
    session["selsubid"]=subid
    return render_template('/College/college_uploadmaterials.html')





@app.route('/college_studymaterialsupload_post',methods=['post'])
def college_studymaterialsupload_post():
    subid=session["selsubid"]
    title=request.form["topic"]
    files=request.files["file"]

    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")

    files.save("D:\\Aproject\\NEWS PORTAL\\web\\SecureID\\SecureID\\static\\Studymaterials\\"+ timestr+".jpg")
    path="/static/Studymaterials/"+ timestr+".jpg"

    qry="INSERT INTO `studymaterials` (`subid`,`title`,`filename`,`fdate`,`clgid`) VALUES ('"+subid+"','"+title+"','"+path+"',CURDATE(),'"+str(session['clg_id'])+"')"
    d=conn()
    d.nonreturn(qry)



    return "<script>alert('Study materials uploaded successfully');window.location='/collegeviewsubjects'</script>"

@app.route('/college_studymaterialsupload_view')
def college_studymaterialsupload_view():
    subid=session["selsubid"]
    qry="SELECT * FROM `studymaterials` WHERE `subid`='"+subid+"' "
    d=conn()
    res=d.selectall(qry)
    return render_template('/College/viewmaterials.html',data=res)

@app.route('/college_dltmaterial/<mid>')
def college_dltmaterial(mid):
    d=conn()
    d.nonreturn("DELETE FROM `studymaterials` WHERE `smid`='"+mid+"'")
    return "<script>alert('Deleted successfully'); window.location='/collegeviewsubjects'</script>"

















@app.route('/edit_placement/<id>')
def edit_placement(id):
    c = conn()
    vc="select * from placement where p_id='"+id+"'"
    va=c.selectone(vc)
    return render_template("College/clg_update_placement.html",data=va)

@app.route('/update_placement',methods=['post'])
def update_placement():
    c = conn()
    stf = request.form['hdname']
    gen = request.form['radio']
    hou = request.form['hname']
    pi = request.form['pin']
    po = request.form['post']
    ph = request.form['cont']
    pid = request.form['pid']
    if 'photo' in request.files:
        im = request.files['photo']
        if im.filename=="":
            st = "update placement set phead_name='" + stf + "',gender='" + gen + "',h_name='" + hou + "',post='" + po + "',pin='" + pi + "',phone='" + ph + "' where p_id='" + pid + "'"
        else:
            dd = str(datetime.datetime.now()).replace(" ", "_").replace("-", "_").replace(":", "_")
            im.save(static_path + "placement_cell\\" + dd + ".jpg")
            path = "/static/placement_cell/" + dd + ".jpg"
            st ="update placement set phead_name='" + stf + "',gender='" + gen + "',h_name='" + hou + "',post='" + po + "',pin='" + pi + "',phone='" + ph + "',photo='" + path + "' where p_id='"+pid+"'"
    else:
        st = "update placement set phead_name='" + stf + "',gender='" + gen + "',h_name='" + hou + "',post='" + po + "',pin='" + pi + "',phone='" + ph + "' where p_id='" + pid + "'"
    c.nonreturn(st)
    return view_cell()

@app.route('/delete_placement/<id>')
def delete_placement(id):
    c = conn()
    da="delete from placement where p_id='"+id+"'"
    c.nonreturn(da)
    return view_cell()

@app.route('/clg_view_std_dept')
def view_std_dpt():
    if session["logout"] == "1":
        c = conn()
        co = "select distinct(department.d_id),department.d_name from course_allocation,course,department where course_allocation.c_id=course.c_id and course.d_id=department.d_id and course_allocation.col_id='" + str(session['clg_id']) + "'"
        cu = c.selectall(co)
        return render_template("College/clg_view std_department.html",data=cu)
    else:
        return login()


@app.route('/ajax_std_dpt',methods=['post'])
def ajax_std_dpt():
    c = conn()
    dep = request.form['dept']
    ce = "select course.c_id,course.c_name from course inner join course_allocation on course.c_id=course_allocation.c_id where course.d_id='" + dep + "' and course_allocation.col_id='"+str(session['clg_id'])+"'"
    res = c.jsonsel(ce)
    return jsonify(res)

@app.route('/ajax_dept_by_clg',methods=['post'])
def ajax_dept_by_clg():
    c = conn()
    clg = request.form['clgid']
    ce = "select distinct(department.d_id),department.d_name from course_allocation,course,department where course_allocation.c_id=course.c_id and course.d_id=department.d_id and course_allocation.col_id='" + clg + "'"
    res = c.jsonsel(ce)
    return jsonify(res)

@app.route('/view_std_dpt',methods=['post'])
def view_view_std():
    c = conn()
    cou=request.form['cou']
    sem=request.form['sem']
    did=request.form['dept']
    session["selsemid"]=sem
    st="select s_name,course.c_name,gender,email,phone,photo,login_id from student,course where student.c_id='"+cou+"' and sem='"+sem+"' and student.d_id='"+did+"' and course.c_id=student.c_id"
    sd=c.selectall(st)
    co = "select distinct(department.d_id),department.d_name from course_allocation,course,department where course_allocation.c_id=course.c_id and course.d_id=department.d_id and course_allocation.col_id='" + str(session['clg_id']) + "'"
    cu = c.selectall(co)
    return render_template("College/clg_view std_department.html",data3=sd,data=cu)

@app.route('/clg_std_view_internal/<sid>')
def clg_std_view_internal(sid):
    if session["logout"] == "1":
        c = conn()
        sem=session["selsemid"]
        ma="select subject.sub,sub_code,internals from subject,internal where internal.s_id='"+sid+"' and subject.sem='"+sem+"' and subject.sub_id=internal.sub_id"
        me=c.selectall(ma)
        return render_template("College/clg_student_internal.html",data=me)

@app.route('/clg_std_view_external/<sid>')
def clg_std_view_external(sid):
    c = conn()
    sem=session["selsemid"]
    me="select subject.sub,sub_code,external from subject,external where external.s_id='"+sid+"' and subject.sem='"+sem+"' and subject.sub_id=external.sub_id"
    ma=c.selectall(me)
    return render_template("College/clg_student_external.html",data=ma)

@app.route('/stf_view_profile')
def stf_view_profile():
    if session["logout"] == "1":
        c = conn()
        sf=" select staff.*,department.d_name from staff,department where staff.dep_name=department.d_id and staff.login_id='"+session["stf_id"]+"'"
        st=c.selectall(sf)
        return render_template("Staff/stf_profile.html",data=st)
    else:
        return login()


@app.route('/stf_view_std')
def stf_view_std():
    if session["logout"] == "1":
        c = conn()
        # ce="select course.c_name,course.c_id from course,staff,department where course.d_id=department.d_id and staff.dep_name=department.d_name and staff.login_id='"+session["stf_id"]+"'"
        ce = "select course.c_name,course.c_id from course,staff where course.d_id=staff.dep_name and staff.login_id='" + session["stf_id"] + "'"
        co=c.selectall(ce)
        return render_template("Staff/stf_view_std.html",data=co)
    else:
        return login()


@app.route('/stf_view_stu',methods=['post'])
def stf_view_stu():
    c = conn()
    co=request.form['cou']
    se=request.form['sem']
    session['sem']=se
    ss="select student.s_name,course.c_name,student.login_id from student,course where student.c_id='"+co+"' and student.sem='"+se+"' and student.c_id=course.c_id"
    st=c.selectall(ss)
    return render_template("Staff/stf_view_std.html",data2=st)

@app.route('/stf_add_internal/<sid>')
def stf_add_int(sid):
    c = conn()
    su="select subject.sub,subject.sub_id from student,subject where student.c_id=subject.c_id and student.login_id='"+sid+"' and subject.sem='"+session['sem']+"'"
    sb=c.selectall(su)
    session['st']=sid
    return render_template("Staff/stf_add_internal.html",data=sb)

@app.route('/add_mark',methods=['post'])
def add_mark():
    sub=request.form['sub']
    mark=request.form['mark']
    st_id=session['st']
    c = conn()
    qr=c.selectone("select * from internal where s_id='"+st_id+"' and sub_id='"+sub+"'")
    if qr is None:
        it="insert into internal values(null,'"+st_id+"','"+sub+"','"+mark+"')"
    else:
        it = "update internal set internals='" + mark + "' where intrn_id='"+str(qr[0])+"'"
    c.nonreturn(it)
    return stf_add_int(st_id)


@app.route('/stf_view_external')
def stf_view_external():
    if session["logout"] == "1":
        c = conn()
        ce ="select course.c_name,course.c_id from course,staff where course.d_id=staff.dep_name and staff.login_id='"+session["stf_id"] +"'"
        co = c.selectall(ce)
        return render_template("Staff/stf_external_mark.html",data=co)
    else:
        return login()


@app.route('/stf_view_ext',methods=['post'])
def stf_view_ext():
    c = conn()
    co = request.form['cou']
    se = request.form['sem']
    ss = "select student.s_name,course.c_name,subject.sub,subject.sub_code,external.mark from student,course,external,subject where student.c_id='"+co+"' and student.sem='"+se+"' and student.c_id=course.c_id and student.s_id=external.s_id and external.sub_id=subject.sub_id"
    st = c.selectall(ss)
    return render_template("Staff/stf_external_mark.html",data2=st)

@app.route('/pla_comp_managmnt')
def pla_comp_manage():
    if session["logout"] == "1":
        return render_template("Placement cell/pla_Company_Management.html")
    else:
        return login()


@app.route('/pla_company_add',methods=['post'])
def pla_company_add():
    comp=request.form['comp']
    phone=request.form['contact']
    ema=request.form['email']
    pla=request.form['place']
    pos=request.form['post']
    pin=request.form['pin']
    pho=request.files['photo']
    lat=request.form['lat']
    log=request.form['log']
    dd=str(datetime.datetime.now()).replace(" ","_").replace(":","_").replace("-","_")
    pho.save(static_path+"company\\"+dd+".jpg")
    path="/static/company/"+dd+".jpg"
    c = conn()
    psw=str(random.randint(0000,9999))
    qr=c.nonreturn("insert into login(username,password,type) values('"+ema+"','"+psw+"','company')")
    cp="insert into company values(null,'"+comp+"','"+path+"','"+pla+"','"+pos+"','"+pin+"','"+ema+"','"+phone+"','"+log+"','"+lat+"','"+str(qr)+"','"+str(session['pla_id'])+"')"
    c.nonreturn(cp)
    return "<script>alert('Company Registered');window.location='/pla_comp_managmnt';</script>"


@app.route('/pla_view_company')
def pla_view_company():
    if session["logout"] == "1":
        c = conn()
        co="select * from company where plcmnt_cell_lid='"+str(session['pla_id'])+"'"
        ce=c.selectall(co)
        return render_template("Placement cell/pla_view_company.html",data=ce)
    else:
        return login()


@app.route('/edit_company/<cmpid>')
def edit_company(cmpid):
    c = conn()
    ca="select * from company where comp_id='"+cmpid+"'"
    cp=c.selectone(ca)
    return render_template("Placement cell/pla_edit_company.html",data=cp)

@app.route('/update_company',methods=['post'])
def update_company():
    comp = request.form['comp']
    phone = request.form['contact']
    pla = request.form['place']
    pos = request.form['post']
    pin = request.form['pin']
    lat = request.form['lat']
    log = request.form['log']
    compid=request.form['compid']
    c = conn()
    if 'image' in request.files:
        pic= request.files['image']
        if pic.filename=="":
            ce = "update company set comp_name='" + comp + "',ph_no='" + phone + "',place='" + pla + "',post='" + pos + "',pin='" + pin + "',lattitude='" + lat + "',longitude='" + log + "' where comp_id='" + compid + "'"
        else:
            dd=str(datetime.datetime.now()).replace(" ","_").replace("-","_").replace(":","_")
            pic.save(static_path+"company\\"+dd+".jpg")
            path="/static/company/"+dd+".jpg"
            ce="update company set photo='"+path+"',comp_name='"+comp+"',ph_no='"+phone+"',place='"+pla+"',post='"+pos+"',pin='"+pin+"',lattitude='"+lat+"',longitude='"+log+"' where comp_id='"+compid+"'"
    else:
        ce = "update company set comp_name='" + comp + "',ph_no='" + phone + "',place='" + pla + "',post='" + pos + "',pin='" + pin + "',lattitude='" + lat + "',longitude='" + log + "' where comp_id='" + compid + "'"
    c.nonreturn(ce)
    return pla_view_company()

@app.route('/delete_company/<comid>')
def delete_company(comid):
    c = conn()
    ca="delete from company where comp_id='"+comid+"'"
    c.nonreturn(ca)
    return pla_view_company()

@app.route('/pla_view_vacancy')
def pla_view_vacancy():
    if session["logout"] == "1":
        c = conn()
        ce="select login_id,comp_name from company where plcmnt_cell_lid='"+str(session['pla_id'])+"'"
        ca=c.selectall(ce)
        return render_template("Placement cell/pla_view_vacancies.html",data=ca)
    else:
        return login()

@app.route('/pla_vacancy',methods=['post'])
def pla_vacancy():
    c = conn()
    co=request.form['company']
    va="select * from vacancy where comp_id='"+co+"'"
    vy=c.selectall(va)
    ce = "select login_id,comp_name from company where plcmnt_cell_lid='" + str(session['pla_id']) + "'"
    ca = c.selectall(ce)
    return render_template("Placement cell/pla_view_vacancies.html",data2=vy,data=ca)

@app.route('/pla_view_shortlists/<vid>')
def pla_view_shortlists(vid):
    if session["logout"] == "1":
        c = conn()
        ce = "select student.*,college.col_name,course.c_name from student,college,course,shortlist where shortlist.s_id=student.login_id and student.col_id=college.login_id and course.c_id=student.c_id and shortlist.v_id='"+vid+"'"
        ca = c.selectall(ce)
        return render_template("Placement cell/pla_view_shortlist.html",data2=ca)
    else:
        return login()

@app.route('/pla_viewmore_shortlist/<sid>')
def viewmore_shortlist(sid):
    c = conn()
    sh = "select student.*,college.col_name,course.c_name,department.d_name from student,college,course,department where department.d_id=student.d_id and student.col_id=college.login_id and course.c_id=student.c_id and student.s_id='"+sid+"'"
    st = c.selectone(sh)
    return render_template("Placement cell/pla_viewmore_shortlist.html",data=st)

@app.route('/std_view_profile')
def std_viewprofile():
    if session["logout"] == "1":
        c = conn()
        st="select student.*,college.col_name,course.c_name from student,college,course where student.login_id='"+session["std_id"]+"' and college.col_id=student.col_id and course.c_id=student.c_id"
        tn=c.selectall(st)
        return render_template("Student/std_view_profile.html",data=tn)
    else:
        return login()


@app.route('/std_internal')
def std_internal():
    if session["logout"] == "1":
        return render_template("Student/std_view_internal.html")
    else:
        return login()

@app.route('/std_view_internal',methods=['post'])
def std_view_internal():
    c = conn()
    sem=request.form['sem']
    it="select subject.sub_code,subject.sub,internal.internals from student,subject,internal where student.login_id='"+session["std_id"]+"' and subject.sem='"+sem+"' and student.login_id=internal.s_id and subject.sub_id=internal.sub_id"
    nt=c.selectall(it)
    return render_template("Student/std_view_internal.html",data=nt)

@app.route('/std_external')
def std_external():
    if session["logout"] == "1":
        return render_template("Student/std_view_external.html")
    else:
        return login()

@app.route('/std_view_external',methods=['post'])
def std_view_external():
    sem=request.form['sem']
    c = conn()
    it="select subject.sub_code,subject.sub,external.mark from subject,external where external.s_id='"+session["std_id"]+"' and subject.sem='"+sem+"' and subject.sub_id=external.sub_id"
    nt=c.selectall(it)
    return render_template("Student/std_view_external.html",data=nt)

@app.route('/std_send_complaint')
def std_send_complaint():
    if session["logout"] == "1":
        c = conn()
        st="select s_id from student where login_id='"+session["std_id"]+"'"
        sa=c.selectone(st)
        return render_template("Student/std_send_complaint.html",data=sa)
    else:
        return login()


@app.route('/std_complaint',methods=['post'])
def std_complaint():
    c = conn()
    cmp=request.form['complaint']
    se="insert into complaint values(null,'"+session["std_id"]+"','"+cmp+"',null,curdate(),'pending')"
    c.nonreturn(se)
    return std_send_complaint()

@app.route('/std_view_reply')
def std_view_reply():
    if session["logout"] == "1":
        c = conn()
        re="select complaint.* from complaint where complaint.s_id='"+session["std_id"]+"'"
        ry=c.selectall(re)
        return render_template("Student/std_view_reply.html",data=ry)
    else:
        return login()

@app.route('/std_delete_reply/<id>')
def std_delete_reply(id):
    c = conn()
    dt="delete from complaint where cm_id='"+id+"'"
    c.nonreturn(dt)
    return std_view_reply()

@app.route('/std_view_vacancy')
def std_view_vacancy():
    if session["logout"] == "1":
        c = conn()
        cm="select * from company"
        co=c.selectall(cm)
        return render_template("Student/std_view_vacancy.html",data=co)
    else:
        return login()

@app.route('/std_vacancy',methods=['post'])
def std_vacancy():
    c = conn()
    co = request.form['company']
    va = "select * from vacancy where comp_id='"+co+"' and v_id not in (select v_id from requests where s_id='"+session['std_id']+"')"
    vy = c.selectall(va)
    cm = "select * from company"
    co = c.selectall(cm)
    return render_template("Student/std_view_vacancy.html",data2=vy,data=co)

@app.route('/std_request_add/<id>')
def std_request_add(id):
    c = conn()
    vy="insert into requests values(null,'"+id+"','"+session['std_id']+"',CURDATE(),'pending')"
    c.nonreturn(vy)
    return std_view_vacancy()

@app.route('/std_view_shortlist')
def std_view_shortlist():
    if session["logout"] == "1":
        c = conn()
        cm="select login_id,comp_name from company"
        co=c.selectall(cm)
        return render_template("Student/std_view_shortlist.html",data=co)
    else:
        return login()


@app.route('/std_shortlist',methods=['post'])
def std_shortlist():
    c = conn()
    co=request.form['company']
    sh="select company.comp_name,vacancy.post from company,vacancy,shortlist where company.login_id='"+co+"' and vacancy.comp_id=company.login_id and vacancy.v_id=shortlist.v_id and shortlist.s_id='"+session['std_id']+"'"
    sl=c.selectall(sh)
    cm = "select login_id,comp_name from company"
    co = c.selectall(cm)
    return render_template("Student/std_view_shortlist.html",data2=sl,data=co)

@app.route('/cmp_add_vacancy')
def cmp_add_vacancy():
    if session["logout"] == "1":
        return render_template("Company/cmp_vacancy_management.html")
    else:
        return login()

@app.route('/cmp_vacancy',methods=['post'])
def cmp_vacancy():
    c = conn()
    po=request.form['post']
    va=request.form['vacancy']
    vy="insert into vacancy values(null,'"+session['cmp_id']+"','"+po+"','"+va+"','pending')"
    c.nonreturn(vy)
    return cmp_add_vacancy()

@app.route('/cmp_view_vacancy')
def cmp_view_vacancy():
    if session["logout"] == "1":
        c = conn()
        cv="select * from vacancy where vacancy.comp_id='"+session['cmp_id']+"'"
        vc=c.selectall(cv)
        return render_template("Company/cmp_view_vacancy.html",data=vc)
    else:
        return login()

@app.route('/cmp_edit_vacancy/<vid>')
def cmp_edit_vacancy(vid):
    c = conn()
    vy="select * from vacancy where v_id='"+vid+"'"
    va=c.selectone(vy)
    return render_template("Company/cmp_edit_vacancy.html",data=va)

@app.route('/cmp_update_vacancy',methods=['post'])
def cmp_update_vacancy():
    c = conn()
    vid=request.form['vid']
    po=request.form['post']
    va=request.form['vacancy']
    ue="update vacancy set post='"+po+"',no_vacancy='"+va+"' where v_id='"+vid+"'"
    c.nonreturn(ue)
    return cmp_view_vacancy()

@app.route('/cmp_delete_vacancy/<vid>')
def cmp_delete_vacancy(vid):
    c = conn()
    dt="delete from vacancy where v_id='"+vid+"'"
    c.nonreturn(dt)
    return cmp_view_vacancy()

@app.route('/cmp_view_vac_reqst/<vid>')
def cmp_view_vac_reqst(vid):
    c = conn()
    dt="select requests.r_id,student.s_name,student.photo,college.col_name,course.c_name,student.sem,student.email,student.phone,requests.date from requests,student,college,course where requests.s_id=student.login_id and student.col_id=college.login_id and student.c_id=course.c_id  and requests.v_id='"+vid+"' and requests.status='pending'"
    res=c.selectall(dt)
    session['vid']=vid
    return render_template("Company/cmp_view_vacancy_request.html",data=res)

@app.route('/cmp_approve_reqst/<rid>')
def cmp_approve_reqst(rid):
    c = conn()
    dt="update requests set status='not-selected' where r_id='"+rid+"'"
    c.nonreturn(dt)
    vid=session['vid']
    return cmp_view_vac_reqst(vid)
@app.route('/cmp_reject_reqst/<rid>')
def cmp_reject_reqst(rid):
    c = conn()
    dt="update requests set status='rejected' where r_id='"+rid+"'"
    c.nonreturn(dt)
    vid=session['vid']
    return cmp_view_vac_reqst(vid)

@app.route("/cmp_add_shortlist")
def cmp_add_shortlist():
    if session["logout"] == "1":
        c=conn()
        qr="select * from vacancy where comp_id='"+str(session['cmp_id'])+"'"
        res=c.selectall(qr)
        return render_template("Company/cmp_shortlist_management.html",data=res)
    else:
        return login()

@app.route("/cmp_add_shortlist_post",methods=['post'])
def cmp_add_shortlist_post():
    btn=request.form['button']
    c=conn()
    if btn=="SEARCH":
        vid=request.form['vcy']
        qry=c.selectall("select requests.r_id,student.s_name,student.photo,college.col_name,course.c_name,student.sem,student.email,student.phone,requests.date from requests,student,college,course where requests.s_id=student.login_id and student.col_id=college.login_id and student.c_id=course.c_id  and requests.v_id='"+vid+"' and requests.status='not-selected'")
        qr="select * from vacancy where comp_id='"+str(session['cmp_id'])+"'"
        res=c.selectall(qr)
        return render_template("Company/cmp_shortlist_management.html",data=res,data2=qry)
    elif btn=="CREATE SHORTLIST":
        ids=request.form.getlist("idd")
        for id in ids:
            qry=c.nonreturn("update requests set status='approved' where r_id='"+id+"'")
            qry2=c.selectone("select v_id,s_id from requests where r_id='"+id+"'")
            qry3=c.nonreturn("insert into shortlist(s_id,v_id) values('"+str(qry2[1])+"','"+str(qry2[0])+"')")
        return "<script>alert('Shortlist Created');window.location='/cmp_add_shortlist';</script>"

@app.route("/cmp_view_shotlist")
def cmp_view_shotlist():
    if session["logout"] == "1":
        c = conn()
        qr = "select * from vacancy where comp_id='" + str(session['cmp_id']) + "'"
        res = c.selectall(qr)
        return render_template("Company/cmp_view_shortlist.html",data=res)
    else:
        return login()
@app.route("/cmp_view_shortlist_post",methods=['post'])
def cmp_view_shortlist_post():
    c = conn()
    vid = request.form['vcy']
    qry = c.selectall("select requests.r_id,student.s_name,student.photo,college.col_name,course.c_name,student.sem,student.email,student.phone,requests.date from requests,student,college,course where requests.s_id=student.login_id and student.col_id=college.login_id and student.c_id=course.c_id  and requests.v_id='" + vid + "' and requests.status='approved'")
    qr = "select * from vacancy where comp_id='" + str(session['cmp_id']) + "'"
    res = c.selectall(qr)
    return render_template("Company/cmp_view_shortlist.html", data=res, data2=qry)

@app.route('/cmp_remove_shortlist/<rid>')
def cmp_remove_shortlist(rid):
    c = conn()
    dt=c.nonreturn("update requests set status='not-selected' where r_id='"+rid+"'")
    qry2 = c.selectone("select v_id,s_id from requests where r_id='" + rid + "'")
    qry3 = c.nonreturn("delete from shortlist where s_id='" + str(qry2[1]) + "' and v_id='" + str(qry2[0]) + "'")
    return cmp_view_shotlist()


@app.route('/cmp_ceo_managemnt')
def cmp_ceo_managemnt():
    if session["logout"] == "1":
        return render_template("Company/cmp_ceo_management.html")
    else:
        return login()

@app.route('/cmp_add_ceo',methods=['post'])
def cmp_add_ceo():
      c = conn()
      con=request.form['ceo']
      va=request.form['radio']
      hn= request.form['hname']
      po = request.form['post']
      pi = request.form['pin']
      pl = request.form['place']
      ph = request.form['phone']
      em = request.form['email']
      pic=request.files['photo']
      dd=str(datetime.datetime.now()).replace(" ","_").replace("-","_").replace(":","_")
      pic.save(static_path+"ceo\\"+dd+".jpg")
      path="/static/ceo/"+dd+".jpg"
      psw=random.randint(0000,9999)
      c = conn()
      qr="select * from ceo where comp_id='"+str(session['cmp_id'])+"'"
      re=c.selectone(qr)

      co = "insert into login values(null,'" + em + "','" + str(psw) + "','ceo')"
      log = c.nonreturn(co)
      if re is None:
          ce="insert into ceo values(null,'"+con+"','"+va+"','"+hn+"','"+po+"','"+pi+"','"+pl+"','"+ph+"','"+em+"','"+path+"','"+str(log)+"','"+str(session['cmp_id'])+"')"
      else:
          ce="update ceo set ceo_name='"+con+"',gender='"+va+"',h_name='"+hn+"',post='"+po+"',pin='"+pi+"',place='"+pl+"',phone='"+ph+"',photo='"+path+"',login_id='"+str(log)+"' where ceo_id='"+str(re[0])+"'"
      c.nonreturn(ce)
      return "<script>alert('CEO Registered');window.location='/cmp_ceo_managemnt';</script>"

@app.route('/cmp_view_ceo')
def cmp_view_ceo():
    if session["logout"] == "1":
        c = conn()
        ce="select * from ceo"
        ba=c.selectall(ce)
        return render_template("Company/cmp_view_ceo.html",data=ba)
    else:
        return login()

@app.route('/cmp_edit_ceo/<cid>')
def cmp_edit_ceo(cid):
    c = conn()
    cd="select * from ceo where ceo_id='"+cid+"'"
    ce=c.selectone(cd)
    return render_template("Company/cmp_edit_ceo.html",data=ce)

@app.route('/cmp_update_ceo',methods=['post'])
def cmp_update_ceo():
    con = request.form['ceo']
    va = request.form['radio']
    hn = request.form['hname']
    po = request.form['post']
    pi = request.form['pin']
    pl = request.form['place']
    ph = request.form['phone']
    cid=request.form['cmpid']
    c = conn()
    if 'photo' in request.files:
        pic = request.files['photo']
        if pic.filename=="":
            up = "update ceo set ceo_name='" + con + "',gender='" + va + "',h_name='" + hn + "',post='" + po + "',pin='" + pi + "',place='" + pl + "',phone='" + ph + "' where ceo_id='" + cid + "'"
        else:
            dd=str(datetime.datetime.now()).replace(" ","_").replace("-","_").replace(":","_")
            pic.save(static_path + "ceo\\" + dd+".jpg")
            path = "/static/ceo/" + dd+".jpg"
            up = "update ceo set ceo_name='" + con + "',gender='" + va + "',h_name='" + hn + "',post='" + po + "',pin='" + pi + "',place='" + pl + "',phone='" + ph + "',photo='" + path + "' where ceo_id='" + cid + "'"
    else:
        up = "update ceo set ceo_name='" + con + "',gender='" + va + "',h_name='" + hn + "',post='" + po + "',pin='" + pi + "',place='" + pl + "',phone='" + ph + "' where ceo_id='" + cid + "'"
    c.nonreturn(up)
    return cmp_view_ceo()

@app.route('/cmp_delete_ceo/<cid>')
def cmp_delete_ceo(cid):
    c = conn()
    dt="delete from ceo where ceo_id='"+cid+"'"
    c.nonreturn(dt)
    return cmp_view_ceo()

@app.route('/verify',methods=['POST'])
def verify():

    imgpath1=""
    imgpath2=""
    img=request.form["img"]

    import base64
    imgdata = base64.b64decode(img)
    filename = r'D:\web\SecureID\static\some_image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)



    qr=request.form["qr"]

    qry="select photo from student where login_id='"+qr+"'"
    cn=conn()
    res=cn.selectone(qry)

    if res is not None:
        import cognitive_face as CF

        KEY = 'd0aa4073ee844c5ba52becc7536a6243'  # Replace with a valid Subscription Key here.
        CF.Key.set(KEY)

        BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
        CF.BaseUrl.set(BASE_URL)

        # img_url = "C:\\Users\\Welcome\\PycharmProjects\\SecureID"+res[0]
        img_url = "D:\web\SecureID" + res[0]
        img_ur2 = "C:\\Users\\Welcome\\PycharmProjects\\SecureID\\static\\some_image.jpg"

        result = CF.face.detect(img_url)
        result2 = CF.face.detect(img_ur2)


        similarity = CF.face.verify(result[0]['faceId'], result2[0]['faceId'])


        if similarity['isIdentical'] == False:
            return jsonify(status="no")
        else:
            return jsonify(status="ok")

    else:
        return jsonify(status="nop")



@app.route("/and_login",methods=['post'])
def and_login():
    usr=request.form['uname']
    psw=request.form['password']
    qry="select * from login where username='"+usr+"' and password='"+psw+"' and type='student'"
    c=conn()
    res=c.selectone(qry)
    if res is not None:
        qry="select * from student where login_id='"+str(res[0])+"'"
        rek=c.selectone(qry)
        if rek is not None:
            return jsonify(status='ok',uid=res[0],sid=rek[0],kk=rek[3],mai=rek[8],im=rek[9])
        else:
            return jsonify(status='no')

        
    else:
        return jsonify(status='no')

@app.route("/and_view_profile",methods=['post'])
def and_view_profile():
    lid=request.form['lid']
    qry="SELECT * FROM student WHERE login_id='"+lid+"'"
    c=conn()
    res=c.selectone(qry)
    if res is not None:
        return jsonify(status='ok',name=res[3],gender=res[2],hname=res[5],post=res[6],pin=res[7],email=res[8],photo=res[9])
    else:
        return jsonify(status='no')



@app.route("/up_profile",methods=['post'])
def up_profile():
    lid=request.form['lid']
    name=request.form['name']
    hn=request.form['hn']
    post=request.form['p']
    pin=request.form['pin']
    email=request.form['em']
    im = request.form["pp"]

    if request.form is not None:

        if "pp" in request.form:

            if request.form["pp"]!='':
                import base64
                a = base64.b64decode(im)
                dt = datetime.datetime.now()
                dd = str(dt).replace(" ", "_").replace(":", "_").replace("-", "_")
                fh = open("D:\\\Aproject\\NEWS PORTAL\\Web\\SecureID\\SecureID\\static\\stud_img\\" + dd + ".jpg","wb")
                path = "/static/stud_img/" + dd + ".jpg"
                fh.write(a)
                fh.close()
                qry="update student set s_name='"+name+"',h_name='"+hn+"',post='"+post+"',pin='"+pin+"',email='"+email+"',photo='"+path+"' where login_id='"+str(lid)+"'"
                c=conn()
                res=c.nonreturn(qry)
                return jsonify(status='ok')
            else:
                qry = "update student set s_name='" + name + "',h_name='" + hn + "',post='" + post + "',pin='" + pin + "',email='" + email + "' where login_id='" + str(lid) + "'"
                c = conn()
                res = c.nonreturn(qry)
                return jsonify(status='ok')

        else:
            qry = "update student set s_name='" + name + "',h_name='" + hn + "',post='" + post + "',pin='" + pin + "',email='" + email + "' where login_id='" + str(
                lid) + "'"
            c = conn()
            res = c.nonreturn(qry)
            return jsonify(status='ok')

    else:
        qry = "update student set s_name='" + name + "',h_name='" + hn + "',post='" + post + "',pin='" + pin + "',email='" + email + "' where login_id='" + str(
            lid) + "'"
        c = conn()
        res = c.nonreturn(qry)
        return jsonify(status='ok')


@app.route('/logout')
def logout():
    session["logout"]="0"
    return login()

@app.route('/andsentfeedback',methods=['post'])
def andsentfeedback():
    cmp=request.form["fdbck"]
    uid=request.form["lid"]
    d=conn()
    q="INSERT INTO `feedback` (`feedback`,`date`,`studentid`) VALUES ('"+cmp+"',CURDATE(),'"+uid+"')"
    d.nonreturn(q)
    return jsonify(status="ok")

@app.route('/andviewalerts',methods=['post'])
def andviewalerts():
    
    d=conn()
    q="SELECT * FROM `alert`"
    res=d.jsonsel(q)
    return jsonify(status="ok",res=res)





@app.route('/andsentcomplaint',methods=['post'])
def andsentcomplaint():
    cmp=request.form["cmp"]
    uid=request.form["uid"]
    d=conn()
    q="INSERT INTO complaint (`s_id`,`cmplaint`,`reply`,`date`,`status`) VALUES ('"+uid+"','"+cmp+"','pending',CURDATE(),'pending')"
    d.nonreturn(q)
    return jsonify(status="ok")

@app.route('/andsentcommmentdiscussion',methods=['post'])
def andsentcommmentdiscussion():
    cmp=request.form["cmp"]
    uid=request.form["uid"]
    did=request.form["did"]
    d=conn()
    q="insert into `comments` (`disid`,`comment`,`cdate`,`studentid`) values ('"+did+"','"+cmp+"',curdate(),'"+uid+"')"
    d.nonreturn(q)
    return jsonify(status="ok")


@app.route('/andviewcomplaint',methods=['post'])
def andviewcomplaint():
    
    uid=request.form["uid"]
    d=conn()
    q="select * from complaint WHERE `s_id`='"+uid+"'"
    res=d.jsonsel(q)
    return jsonify(status="ok",res=res)




@app.route('/and_logins',methods=['post'])
def and_logins():
    uname=request.form["uname"]
    password=request.form["password"]

    d=conn()
    qry="SELECT * FROM login WHERE username='"+uname+"' AND PASSWORD='"+password+"' AND TYPE='student'"
    res=d.selectone(qry)
    if res is not None:
        return jsonify(status='ok',uid=res[0])
    else:
        return jsonify(status='no')


@app.route("/and_view_profiles", methods=['post'])
def and_view_profiles():
    lid = request.form['lid']
    qry = "SELECT * FROM student WHERE login_id='" + lid + "'"
    c = conn()
    res = c.selectone(qry)
    if res is not None:
        return jsonify(status='ok', name=res[3], gender=res[2], hname=res[5], post=res[6], pin=res[7], email=res[8],photo=res[9])
    else:
        return jsonify(status='no')

@app.route('/andrating',methods=['post'])
def and_ratings():
    lid=request.form["lid"]
    rating=request.form["rating"]
    d=conn()
    d.nonreturn("INSERT INTO rating (`rating`,`studentid`,rdate) VALUES ('"+rating+"','"+lid+"',CURDATE())")
    return jsonify(status="ok")
@app.route('/and_newdiscussion',methods=['post'])
def and_newdiscussion():
    lid=request.form["lid"]
    msg=request.form["msg"]
    d=conn()
    d.nonreturn("INSERT INTO `discussion` (`studentid`,`message`,`msgdate`) VALUES ('"+lid+"','"+msg+"',curdate())")
    return jsonify(status="ok")

@app.route('/and_viewalldiscusion',methods=['post'])
def and_viewalldiscusion():
    d=conn()
    qry="SELECT `discussion`.*,`student`.* FROM `discussion` INNER JOIN `student` ON `student`.`login_id`=`discussion`.`studentid`"
    res=d.jsonsel(qry)
    return jsonify(status='ok',res=res)


@app.route('/adminviewfeedback')
def adminviewfeedback():
    d=conn()
    qry="SELECT `feedback`.*,`student`.* FROM feedback,student WHERE `feedback`.`studentid`=`student`.`login_id`"
    res=d.selectall(qry)
    return render_template('admin/view_feeback.html',res=res)

@app.route('/adminviewratings')
def adminviewratings():
    d=conn()
    qry="SELECT `rating`.*,`student`.* FROM rating,student WHERE `rating`.`studentid`=`student`.`login_id`"
    res=d.selectall(qry)
    return render_template('admin/adm_view_rating.html',res=res)

@app.route('/clg_discussion')
def clg_discussion():
    d=conn()
    qry="SELECT discussion.*,student.* FROM `discussion`,`student` WHERE student.`login_id`=`discussion`.`studentid` and student.col_id='"+session['clg_id']+"'"
    res=d.selectall(qry)
    return render_template('College/view_discussion.html',res=res)

@app.route('/clg_view_comments/<id>')
def clg_view_comments(id):
    d=conn()
    qry="SELECT `comments`.*,`discussion`.*,`student`.* FROM `comments`,`discussion`,`student` WHERE `comments`.`disid`=`discussion`.`discussionid` AND `comments`.`studentid`=`student`.`login_id` AND `discussion`.`discussionid`='"+id+"'"
    res=d.selectall(qry)
    return render_template('College/view_comments.html',res=res)

@app.route('/clg_view_articles')
def clg_view_articles():
    d=conn()
    qry="SELECT `article`.*,`student`.* FROM `article`,`student` WHERE `article`.`student_id`=`student`.`login_id` AND student.`col_id`='"+session['clg_id']+"'"
    res=d.selectall(qry)
    return render_template('College/view_article.html',res=res)


@app.route('/and_vieallcommentsbydid',methods=['POST'])
def and_vieallcommentsbydid():
    did=request.form["did"]
    db=conn()
    qry="SELECT `comments`.*,`student`.*  FROM comments,student WHERE `comments`.`studentid`=`student`.`login_id` AND `comments`.`disid`='"+did+"'"
    res=db.jsonsel(qry)
    return jsonify(status="ok",res=res)
    


@app.route('/and_addcmment',methods=['post'])
def and_addcmment():
    disid=request.form["did"]
    comment=request.form["comment"]
    sid=request.form["uid"]
    qry="INSERT INTO `comments`(`disid`,`comment`,`cdate`,`studentid`) VALUES ('"+disid+"','"+comment+"',CURDATE(),'"+sid+"')"
    d=conn()
    d.nonreturn(qry)
    return jsonify(status="ok")

@app.route('/and_Viewsubjects',methods=['post'])
def and_Viewsubjects():
    d=conn()
    lid=request.form["uid"]
    qry="SELECT * FROM `subject` WHERE `c_id` IN (SELECT `c_id` FROM `student` WHERE `login_id`='"+lid+"')"
    res=d.jsonsel(qry)
    return jsonify(status="ok",data=res)


@app.route('/and_Viewstudymaterials',methods=['post'])
def and_viewmaterials():
    sid=request.form["sid"]
    qry="SELECT * FROM `studymaterials` WHERE subid='"+sid+"'"
    c=conn()
    res=c.jsonsel(qry)
    return jsonify(status="ok",data=res)


@app.route('/and_viewallarticles',methods=['post'])
def and_viewallarticles():
    qry="SELECT `article`.*,`student`.* FROM article,student WHERE article.`student_id`=`student`.`login_id`"
    d=conn()
    res=d.jsonsel(qry)
    return jsonify(status='ok',res=res)



@app.route('/and_delarticle',methods=['post'])
def and_deletearticle():
    id=request.form["aid"]
    d=conn()
    d.nonreturn("delete from article where article_id='"+id+"'")
    return jsonify(status="ok")




@app.route('/delcomp',methods=['post'])
def delcomp():
    id=request.form["cid"]
    d=conn()
    d.nonreturn("delete from complaint where cm_id='"+id+"'")
    return jsonify(status="ok")


@app.route('/and_addcmment_art',methods=['post'])
def and_addcmment_art():
    aid=request.form["aid"]
    comment=request.form["comment"]
    sid=request.form["uid"]
    qry="INSERT INTO `comments_art`(`aid`,`comment`,`cdate`,`studentid`) VALUES ('"+aid+"','"+comment+"',CURDATE(),'"+sid+"')"
    d=conn()
    d.nonreturn(qry)
    return jsonify(status="ok")

@app.route('/and_vieallcomments_article_byaid',methods=['POST'])
def and_vieallcomments_article_byaid():
    did=request.form["did"]
    db=conn()
    qry="SELECT `comments_art`.*,`student`.*  FROM comments_art,student WHERE `comments_art`.`studentid`=`student`.`login_id` AND `comments_art`.`aid`='"+did+"'"
    res=db.jsonsel(qry)
    return jsonify(status="ok",res=res)

@app.route('/admin_Addnotification')
def admin_Addnotification():
    return render_template('/admin/adm_alertadd.html')

@app.route('/admin_Addnotification_post',methods=['post'])
def admin_Addnotification_post():
    notifi=request.form["notificaton"]
    d=conn()
    qry="INSERT INTO `alert` (`alertname`,`date`) VALUES ('"+notifi+"',CURDATE())"
    d.nonreturn(qry)
    return "<script>alert('Added Successfully');window.location='/admin_Addnotification'</script>"

@app.route('/admin_viewnotification')
def admin_viewnotification():
    d=conn()
    res=d.selectall("select * from alert")
    return render_template('/admin/adm_view_alert.html',data=res)

@app.route('/delete_alert/<aid>')
def delete_alert(aid):
    d=conn()
    qry="delete from alert where alert_id='"+aid+"'"
    d.nonreturn(qry)
    return "<script>alert('Notification Deleted successfully');window.location='/admin_viewnotification'</script>"

@app.route('/forget_password')
def forget_password():
    return render_template('resetpswd.html')


@app.route('/fpass',methods=['post'])
def fpass():

    ml=request.form["txt_uname"]

    qry="select password from login where username='"+ml+"'"
    db=conn()

    ress=db.selectone(qry)
    if ress is not None:
        import smtplib

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("jdtbcaproject@gmail.com", "newsportal")
        from email.mime.multipart import MIMEMultipart
        msg = MIMEMultipart()  # create a message.........."
        message = "Messege from News Portal"
        msg['From'] = "jdtbcaproject@gmail.com"
        msg['To'] = ml
        msg['Subject'] = "Your Password"
        body = "Your Password- " + str(ress[0])
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)

        return "<script>alert('Details updated');window.location='/';</script>"
    else:
        return "<script>alert('Invalid email details');window.location='/';</script>"


@app.route('/and_newarticle',methods=['post'])
def and_newarticle():
    lid=request.form["lid"]
    msg=request.form["msg"]
    filecon=request.form["file"]
    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    import base64
    a=base64.b64decode(filecon)
    fh = open("D:\\Aproject\\NEWS PORTAL\\Web\\SecureID\\SecureID\\static\\article\\"+str(timestr)+".jpg", "wb")
    fh.write(a)
    fh.close()





    path="/static/article/"+timestr+".jpg"
    d=conn()
    d.nonreturn("INSERT INTO `article` (`student_id`,`file`,`date`,`description`) VALUES ('"+lid+"','"+path+"',CURDATE(),'"+msg+"')")
    return jsonify(status="ok")


if __name__ == '__main__':
    app.run(debug=True,port=4000,host='0.0.0.0')

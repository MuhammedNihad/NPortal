/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.6.12-log : Database - secure_id
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`secure_id` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `secure_id`;

/*Table structure for table `ceo` */

DROP TABLE IF EXISTS `ceo`;

CREATE TABLE `ceo` (
  `ceo_id` int(11) NOT NULL AUTO_INCREMENT,
  `ceo_name` varchar(50) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `h_name` varchar(20) DEFAULT NULL,
  `post` varchar(20) DEFAULT NULL,
  `pin` varchar(11) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  `comp_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`ceo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `ceo` */

insert  into `ceo`(`ceo_id`,`ceo_name`,`gender`,`h_name`,`post`,`pin`,`place`,`phone`,`email`,`photo`,`login_id`,`comp_id`) values (3,'fgfj','female','hlo','kochi','8778','k',65798690,'jis@gmail.com','/static/ceo/Untitled.png',9,8);

/*Table structure for table `college` */

DROP TABLE IF EXISTS `college`;

CREATE TABLE `college` (
  `col_id` int(11) NOT NULL AUTO_INCREMENT,
  `col_name` varchar(50) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  `ph_no` bigint(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `pin` varchar(20) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`col_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `college` */

insert  into `college`(`col_id`,`col_name`,`photo`,`ph_no`,`email`,`post`,`pin`,`place`,`login_id`) values (1,'abc','aaa',1234,'adfgh','tirur','676423','asbnm,,',2),(2,'gfe','bbb',3456,'gvvj',NULL,NULL,'vfd',3),(5,'bnm','efvt',987,'mjki',NULL,NULL,'gtdr',4),(6,'Mcas','/static/clg/2.png',9008007007,'mcas@gmail.com','vengara','676311','vengara',10),(7,'Mcas','/static/clg/Untitled.png',7098654653,'jishnu123@gmail.com','vengara','676317','kochi',11);

/*Table structure for table `company` */

DROP TABLE IF EXISTS `company`;

CREATE TABLE `company` (
  `comp_id` int(11) NOT NULL AUTO_INCREMENT,
  `comp_name` varchar(30) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  `place` varchar(20) DEFAULT NULL,
  `post` varchar(20) DEFAULT NULL,
  `pin` varchar(11) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `ph_no` bigint(20) DEFAULT NULL,
  `longitude` varchar(20) DEFAULT NULL,
  `lattitude` varchar(20) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`comp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `company` */

insert  into `company`(`comp_id`,`comp_name`,`photo`,`place`,`post`,`pin`,`email`,`ph_no`,`longitude`,`lattitude`,`login_id`) values (1,'tcs','Untitled.png','calicut','kozhikode','676312','shuhaib123@gmail.com',7434758465,'56 S','56 N',8),(2,'ght','Untitled.png','kochi','aluva','676311','shuhaib123@gmail.com',74377780,'56 S','56 N',12);

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `cm_id` int(11) NOT NULL AUTO_INCREMENT,
  `s_id` int(11) DEFAULT NULL,
  `cmplaint` varchar(200) DEFAULT NULL,
  `reply` varchar(200) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`cm_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`cm_id`,`s_id`,`cmplaint`,`reply`,`date`,`status`) values (10,101,'it is a complaint','done','12-10-2019','replied');

/*Table structure for table `course` */

DROP TABLE IF EXISTS `course`;

CREATE TABLE `course` (
  `c_id` int(11) NOT NULL AUTO_INCREMENT,
  `d_id` int(11) DEFAULT NULL,
  `c_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

/*Data for the table `course` */

insert  into `course`(`c_id`,`d_id`,`c_name`) values (1,7,'bba'),(2,12,'mfc'),(8,7,'bcom'),(9,5,'psy1'),(10,6,'psy'),(11,5,'pp'),(12,0,'hbuy'),(13,3,'gv ');

/*Table structure for table `course_allocation` */

DROP TABLE IF EXISTS `course_allocation`;

CREATE TABLE `course_allocation` (
  `ca_id` int(11) NOT NULL AUTO_INCREMENT,
  `col_id` int(11) DEFAULT NULL,
  `c_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`ca_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;

/*Data for the table `course_allocation` */

insert  into `course_allocation`(`ca_id`,`col_id`,`c_id`) values (1,1,2),(5,2,5),(6,2,5),(7,2,5),(8,2,5),(9,2,7),(10,2,7),(11,0,2),(12,5,1),(13,0,2),(14,2,8),(15,2,2),(16,1,3),(17,1,8);

/*Table structure for table `department` */

DROP TABLE IF EXISTS `department`;

CREATE TABLE `department` (
  `d_id` int(11) NOT NULL AUTO_INCREMENT,
  `d_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`d_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

/*Data for the table `department` */

insert  into `department`(`d_id`,`d_name`) values (3,'doc'),(5,'fyg'),(6,'asx'),(7,'commerece'),(12,'computer science');

/*Table structure for table `external` */

DROP TABLE IF EXISTS `external`;

CREATE TABLE `external` (
  `ex_id` int(11) NOT NULL AUTO_INCREMENT,
  `s_id` int(11) DEFAULT NULL,
  `sub_id` int(11) DEFAULT NULL,
  `external` int(11) DEFAULT NULL,
  PRIMARY KEY (`ex_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `external` */

insert  into `external`(`ex_id`,`s_id`,`sub_id`,`external`) values (1,101,7,43),(2,103,4,49);

/*Table structure for table `internal` */

DROP TABLE IF EXISTS `internal`;

CREATE TABLE `internal` (
  `intrn_id` int(11) NOT NULL AUTO_INCREMENT,
  `s_id` int(11) DEFAULT NULL,
  `sub_id` int(11) DEFAULT NULL,
  `internals` int(11) DEFAULT NULL,
  PRIMARY KEY (`intrn_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

/*Data for the table `internal` */

insert  into `internal`(`intrn_id`,`s_id`,`sub_id`,`internals`) values (1,103,8,19),(2,103,4,20),(15,101,7,16),(16,101,8,15);

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`type`) values (1,'admin','admin','admin'),(2,'college','college','college'),(3,'staff','staff','staff'),(6,'placement','placement','placement'),(7,'student','student','student'),(8,'company','company','company'),(9,'jis@gmail.com','5901','ceo'),(10,'mcas@gmail.com','3166','college'),(11,'jishnu123@gmail.com','3166','college');

/*Table structure for table `placement` */

DROP TABLE IF EXISTS `placement`;

CREATE TABLE `placement` (
  `p_id` int(11) NOT NULL AUTO_INCREMENT,
  `phead_name` varchar(50) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `h_name` varchar(20) DEFAULT NULL,
  `post` varchar(20) DEFAULT NULL,
  `pin` varchar(11) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`p_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `placement` */

insert  into `placement`(`p_id`,`phead_name`,`gender`,`h_name`,`post`,`pin`,`phone`,`email`,`photo`,`login_id`) values (2,'sudheep','male','hlo','hghjg','808',8687970,'Dilshaddilu728@gmail','2.png',2);

/*Table structure for table `requests` */

DROP TABLE IF EXISTS `requests`;

CREATE TABLE `requests` (
  `r_id` int(11) NOT NULL AUTO_INCREMENT,
  `col_id` int(11) DEFAULT NULL,
  `d_id` int(11) DEFAULT NULL,
  `c_id` int(11) DEFAULT NULL,
  `sem` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  PRIMARY KEY (`r_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

/*Data for the table `requests` */

insert  into `requests`(`r_id`,`col_id`,`d_id`,`c_id`,`sem`,`status`,`date`,`year`) values (1,2,NULL,3,NULL,'999','ghh',NULL),(2,2,NULL,3,999,'ghh','65',NULL),(3,1,2,3,999,'pending','2011-01-08',NULL),(4,2,NULL,2,2021,'confirmed','2011-01-12',NULL),(5,2,4,1,2022,'Pending','2011-01-12',NULL),(6,2,4,1,2022,'Pending','2011-01-12',NULL),(7,2,7,8,2021,'Pending','2011-01-12',NULL),(8,2,7,8,2021,'Pending','2011-01-12',NULL),(9,2,7,8,2021,'Pending','2011-01-12',NULL),(10,2,4,5,2019,'Pending','2011-01-15',NULL),(11,2,4,5,2019,'Pending','2011-01-15',NULL),(12,1,7,1,2019,'Pending','2019-10-30',NULL),(13,5,7,1,2020,'Pending','2019-11-24',NULL),(14,1,12,2,1,'confirmed','2019-12-31',2020);

/*Table structure for table `shortlist` */

DROP TABLE IF EXISTS `shortlist`;

CREATE TABLE `shortlist` (
  `sh_id` int(11) NOT NULL AUTO_INCREMENT,
  `s_id` int(11) DEFAULT NULL,
  `v_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`sh_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `shortlist` */

insert  into `shortlist`(`sh_id`,`s_id`,`v_id`) values (1,101,1);

/*Table structure for table `staff` */

DROP TABLE IF EXISTS `staff`;

CREATE TABLE `staff` (
  `staf_id` int(11) NOT NULL AUTO_INCREMENT,
  `st_name` varchar(20) DEFAULT NULL,
  `dep_name` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `h_name` varchar(20) DEFAULT NULL,
  `post` varchar(20) DEFAULT NULL,
  `pin` varchar(11) DEFAULT NULL,
  `ph_no` bigint(20) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  `qual` varchar(50) DEFAULT NULL,
  `experience` varchar(20) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`staf_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `staff` */

insert  into `staff`(`staf_id`,`st_name`,`dep_name`,`gender`,`h_name`,`post`,`pin`,`ph_no`,`email`,`photo`,`qual`,`experience`,`login_id`) values (1,'jaseer','computer science','Male','yfyjgu','vengara','676312',987757987,'jaseer123@gmail.com','Untitled.png','Mca,net',' 5 years',3),(2,'Jishnu','computer science','Male','parayil','vengara','676312',7098654653,'jishnu123@gmail.com','2.png','Mca,net','3 years',4),(5,'Jishnu','computer science','Male','parayil','vengara','676312',7098654653,'jishnu123@gmail.com','2.png','Mca,net','3 years',6);

/*Table structure for table `student` */

DROP TABLE IF EXISTS `student`;

CREATE TABLE `student` (
  `s_id` int(11) NOT NULL AUTO_INCREMENT,
  `col_id` int(11) DEFAULT NULL,
  `c_id` int(11) DEFAULT NULL,
  `s_name` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `h_name` varchar(20) DEFAULT NULL,
  `post` varchar(30) DEFAULT NULL,
  `pin` varchar(11) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  `sem` int(11) DEFAULT NULL,
  `batch` varchar(10) DEFAULT NULL,
  `d_id` int(11) DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  PRIMARY KEY (`s_id`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=latin1;

/*Data for the table `student` */

insert  into `student`(`s_id`,`col_id`,`c_id`,`s_name`,`gender`,`h_name`,`post`,`pin`,`email`,`photo`,`login_id`,`sem`,`batch`,`d_id`,`phone`) values (101,1,2,'rahul','male',NULL,NULL,NULL,NULL,'hdjj',7,6,NULL,12,NULL),(103,1,2,'shuhaib','Male','yuyiu','vengara','676312','jishnu123@gmail.com','fgf',2,2,'2017-20',NULL,65798690);

/*Table structure for table `subject` */

DROP TABLE IF EXISTS `subject`;

CREATE TABLE `subject` (
  `sub_id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `sub` varchar(15) DEFAULT NULL,
  `sub_code` varchar(10) DEFAULT NULL,
  `sem` int(11) DEFAULT NULL,
  PRIMARY KEY (`sub_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `subject` */

insert  into `subject`(`sub_id`,`c_id`,`sub`,`sub_code`,`sem`) values (1,9,'phys','p00',1),(2,5,'yuh','uki',2),(4,8,'accounting','ac1',2),(5,9,'physicology','pgy',4),(7,2,'business','bb',5),(8,2,'qt','qty',2);

/*Table structure for table `subject_allocation` */

DROP TABLE IF EXISTS `subject_allocation`;

CREATE TABLE `subject_allocation` (
  `subal_id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `sub_id` int(11) DEFAULT NULL,
  `sem` int(11) DEFAULT NULL,
  PRIMARY KEY (`subal_id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;

/*Data for the table `subject_allocation` */

insert  into `subject_allocation`(`subal_id`,`c_id`,`sub_id`,`sem`) values (1,0,1,5),(2,0,5,4),(4,1,3,3),(11,0,1,2),(12,0,0,6),(13,0,0,6),(14,0,0,2),(15,0,0,2),(16,0,2,4),(17,0,2,2),(18,0,5,2),(19,0,5,2),(20,0,7,2),(21,0,4,2),(22,0,1,1),(24,1,4,1),(30,0,2,1),(31,10,1,6),(33,0,2,1),(36,11,7,5),(38,11,5,2),(42,1,8,4);

/*Table structure for table `vacancy` */

DROP TABLE IF EXISTS `vacancy`;

CREATE TABLE `vacancy` (
  `v_id` int(11) NOT NULL AUTO_INCREMENT,
  `comp_id` int(11) DEFAULT NULL,
  `post` varchar(30) DEFAULT NULL,
  `no_vacancy` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`v_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `vacancy` */

insert  into `vacancy`(`v_id`,`comp_id`,`post`,`no_vacancy`,`status`) values (1,1,'trainee',5,'pending'),(2,8,'swtester',8,'pending');

/*Table structure for table `vacancy_request` */

DROP TABLE IF EXISTS `vacancy_request`;

CREATE TABLE `vacancy_request` (
  `vr_id` int(11) NOT NULL AUTO_INCREMENT,
  `v_id` int(11) DEFAULT NULL,
  `s_id` int(11) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`vr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `vacancy_request` */

insert  into `vacancy_request`(`vr_id`,`v_id`,`s_id`,`date`,`status`) values (1,1,7,'2019-12-26','pending');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;

CREATE SCHEMA `roboter` DEFAULT CHARACTER SET utf8 ;


CREATE TABLE `roboter`.`bbs_member` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '自动编号',
  `username` VARCHAR(45) NOT NULL COMMENT '账户名',
  `password` VARCHAR(45) NOT NULL COMMENT '账户密码',
  `email` VARCHAR(45) NOT NULL COMMENT '邮箱',
  `dz_uid` INT DEFAULT 0 COMMENT '论坛的uid',
  `create_datetime` timestamp NOT NULL COMMENT '添入时间',
  PRIMARY KEY (`id`)  COMMENT '自动注册用户');


CREATE TABLE `roboter`.`bbs_attachment` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '自动编号',
  `file_name` VARCHAR(255) NOT NULL COMMENT '文件名',
  `key_name` VARCHAR(80) DEFAULT '' COMMENT '七牛文件名',
  `down_link` VARCHAR(150) DEFAULT '' COMMENT '下载地址',
  `md5sum` VARCHAR(80) DEFAULT '' COMMENT '文件信息摘要Hash',
  `plate` INT DEFAULT 0 COMMENT '版块',
  `status` INT DEFAULT 0 COMMENT '是否发帖(0:未传;1:已传;2:已发)',
  `author` VARCHAR(45) DEFAULT '' COMMENT '所属用户',
  `create_datetime` timestamp NOT NULL COMMENT '添入时间',
  `upload_datetime` timestamp NULL COMMENT '上传时间',
  PRIMARY KEY (`id`)  COMMENT '自动上传七牛文件');


CREATE TABLE `roboter`.`bbs_surplus` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '自动编号',
  `fid` INT DEFAULT 0 COMMENT '版块',
  `path` VARCHAR(255) NOT NULL COMMENT '文件名',
  `md5sum` VARCHAR(80) DEFAULT '' COMMENT '文件信息摘要Hash',
  `plate` INT DEFAULT 0 COMMENT '版块',
  `author` VARCHAR(45) DEFAULT '' COMMENT '所属用户',
  `create_datetime` timestamp NOT NULL COMMENT '记录时间',
  PRIMARY KEY (`id`)  COMMENT '文件重复日志');


CREATE TABLE `roboter`.`bbs_thread` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '自动编号',
  `thread_id` INT NOT NULL COMMENT '主题ID',
  `post_id` INT NOT NULL COMMENT '帖子ID',
  `attachment_id` INT DEFAULT 0 COMMENT '附件ID',
  `robot_data_id` INT DEFAULT 0 COMMENT '入库文件ID',
  `create_datetime` timestamp NOT NULL COMMENT '添入时间',
  PRIMARY KEY (`id`)  COMMENT '自动发文件帖子');


CREATE TABLE `roboter`.`bbs_post` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '自动编号',
  `uid` INT NOT NULL DEFAULT 0 COMMENT 'Dz用户Id',
  `tid` VARCHAR(45) NOT NULL DEFAULT 0 COMMENT 'Dz主题Id',
  `pid` INT NOT NULL DEFAULT 0 COMMENT 'Dz帖子Id',
  `create_datetime` timestamp NOT NULL COMMENT '自动回帖时间',
  PRIMARY KEY (`id`) COMMENT '自动回帖');


ALTER TABLE `roboter`.`bbs_attachment` ADD INDEX( `status`);
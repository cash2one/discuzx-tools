# 查询论坛版块
# fid 版块Id; name 版块名称; status 显示状态 (0:隐藏 1:正常 3:群组)
SELECT fid, name FROM `bbs_forum_forum` WHERE status=1 AND type= 'forum';

# coding:utf-8

import pymysql


class Test(object):
    def __init__(self, conn):
        self.conn = conn

    # 获取公司数据库
    @staticmethod
    def get_db(comp_id):
        cursor = conn.cursor()
        sql = "SELECT name from xx WHERE comp_id = %d" % comp_id
        cursor.execute(sql)
        rs = cursor.fetchall()
        return rs

    @staticmethod
    def del_tables_record(conn, db, tables_name, filed_name, user_id, comp_id=None):
        print "正在删除%s数据库中的%s表记录......" % (db, tables_name)
        cursor = conn.cursor()
        if not comp_id:
            sql = "DELETE FROM %s WHERE %s = %d" % (tables_name, filed_name, user_id)
        else:
            sql = "DELETE FROM xx WHERE comp_id = %d and user_id = %d" % (comp_id, user_id)
        cursor.execute(sql)
        cursor.close()

    @staticmethod
    def del_task_record(conn, user_id):
        cursor = conn.cursor()
        select_sql = "SELECT * FROM xx WHERE create_user_id = %d" % user_id
        cursor.execute(select_sql)
        rs = cursor.fetchall()
        parent_taks = []
        child_task = []
        for task in rs:
            if task[13]:
                child_task.append(task)
            else:
                parent_taks.append(task)
        for task in child_task:
            del_sql = "DELETE FROM xx WHERE id = %d" % task[0]
            cursor.execute(del_sql)

        for task in parent_taks:
            del_sql = "DELETE FROM xx WHERE id = %d" % task[0]
            cursor.execute(del_sql)

    # 删除公司库中用户记录
    def del_comp_userinfo(self, conn, user_id):
        try:
            # 外出打卡
            Test.del_tables_record(conn, "公司", "xx", "create_user_id", user_id)  # 删除公司数据库中signin表中的记录
            # 工作汇报
            Test.del_tables_record(conn, "公司", "xx", "create_user_id", user_id)  # 删除公司数据库中daily_template表中的记录
            Test.del_tables_record(conn, "公司", "xx", "create_user_id", user_id)  # 删除公司数据库中daily_mf表中的记录
            Test.del_tables_record(conn, "公司", "xx", "create_user_id", user_id)  # 删除公司数据库中daily_permission表中的记录
            # 公告
            Test.del_tables_record(conn, "公司", "xx", "UsrID", user_id)  # 删除公司数据库中notice_mf表中的记录
            Test.del_tables_record(conn, "公司", "xx", "user_id", user_id)  # 删除公司数据库中notice_create_usr表中的记录
            # 流程
            Test.del_tables_record(conn, "公司", "xx", "create_user_id", user_id)  # 删除公司数据库中workflow_template表中的记录
            Test.del_tables_record(conn, "公司", "xx", user_id)  # 删除公司数据库中daily_mf表中的记录
            Test.del_tables_record(conn, "公司", "xx", "create_user_id", user_id)  # 删除公司数据库中daily_permission表中的记录
            # 日程提醒
            Test.del_tables_record(conn, "公司", "xx", "create_user_id", user_id)  # 删除公司数据库中schedule表中的记录
            # 考勤
            Test.del_tables_record(conn, "公司", "xx", "user_id", user_id)  # 删除公司数据库中workatd_autocheckin表中的记录
            Test.del_tables_record(conn, "公司", "xx", "user_id", user_id)  # 删除公司数据库中workatd_withoutusr表中的记录
            Test.del_tables_record(conn, "公司", "xx", "user_id", user_id)  # 删除公司数据库中workatd_checkin表中的记录
            Test.del_tables_record(conn, "公司", "xxr", "user_id", user_id)  # 删除公司数据库中workatd_reportusr表中的记录
            # 任务
            Test.del_task_record(conn, user_id)  # 删除公司数据库中workatd_autocheckin表中的记录
            # 报销
            Test.del_tables_record(conn, "公司", "xx", "create_user_id", user_id)  # 删除公司数据库中workatd_autocheckin表中的记录
            Test.del_tables_record(conn, "公司", "xx", "verifier_id", user_id)  # 删除公司数据库中workatd_autocheckin表中的记录
            # 用戶
            Test.del_tables_record(conn, "公司", "xx", "user_id", user_id)  # 删除公司数据库中srv_usr表中的记录
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

    # 删除core中用户记录
    def del_core_userinfo(self, comp_id, conn, user_id):
        try:
            self.del_tables_record(conn, "xx", "xx", "user_id", user_id)  # 删除core数据库中sys_usr表中的记录
            self.del_tables_record(conn, "xx", "xxx", "user_id", user_id, comp_id)  # 删除core数据库中sys_comp_usr表中的记录
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e


if __name__ == "__main__":
    comp_id = input("请输入您要删除的公司代号：")
    user_id = input("请输入您要删除的用户id：")

    core_conn = pymysql.connect(host="xxxxx", port=1111, user="xxx", passwd="xxx", db="xxx", charset="utf8")

    # 获取公司数据库
    conn = core_conn
    test = Test(conn)
    db = test.get_db(comp_id)

    # 删除公司数据库中的用户信息
    conn = pymysql.connect(host="xxxxx", port=1111, user="xxx", passwd="xxx", db=db[0][0], charset="utf8")
    test = Test(conn)
    sql = "DELETE FROM xxx WHERE id = %d" % user_id
    try:
        test.del_comp_userinfo(conn, user_id)
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    conn.close()

    # 删除core中的用户信息
    try:
        conn = core_conn
        test.del_core_userinfo(comp_id, conn, user_id)
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    conn.close()

    print "删除成功！"

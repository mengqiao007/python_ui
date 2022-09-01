DROP TABLE IF EXISTS service;
CREATE TABLE service(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '服务ID' ,
    service_name VARCHAR(32) NOT NULL   COMMENT '服务名称' ,
    service_domain VARCHAR(255)    COMMENT '服务域' ,
    service_detail VARCHAR(255)    COMMENT '服务详情' ,
    service_ext VARCHAR(255)    COMMENT '服务扩展属性' ,
    status INT   DEFAULT 1 COMMENT '服务状态' ,
    CREATED_BY VARCHAR(32)    COMMENT '创建人' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_BY VARCHAR(32)    COMMENT '更新人' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
)  COMMENT = '所属服务' engine = innodb default charset = utf8;

DROP TABLE IF EXISTS version;
CREATE TABLE version(
    id INT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    version VARCHAR(32) NOT NULL   COMMENT '版本号' ,
    CREATED_BY VARCHAR(32)    COMMENT '创建人' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_BY VARCHAR(32)    COMMENT '更新人' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
)  COMMENT = '版本号' engine = innodb default charset = utf8;

DROP TABLE IF EXISTS module;
CREATE TABLE module(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '模块ID' ,
    module_name VARCHAR(255) NOT NULL   COMMENT '模块名称' ,
    service_id VARCHAR(32)    COMMENT '服务ID' ,
    service_name VARCHAR(255)    COMMENT '服务名称' ,
    version_id VARCHAR(255)    COMMENT '版本ID' ,
    version VARCHAR(255)    COMMENT '版本号' ,
    status VARCHAR(255)   DEFAULT 1 COMMENT '模块状态' ,
    CREATED_BY VARCHAR(32)    COMMENT '创建人' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_BY VARCHAR(32)    COMMENT '更新人' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
)  COMMENT = '接口模块' engine = innodb default charset = utf8;

DROP TABLE IF EXISTS test_case;
CREATE TABLE test_case(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '测试用例ID' ,
    name VARCHAR(32) NOT NULL   COMMENT '测试用例名称' ,
    module_id INT   COMMENT '模块ID' ,
    module_name VARCHAR(255)   COMMENT '模块名称' ,
    service_id VARCHAR(32)    COMMENT '服务ID' ,
    service_name VARCHAR(255)    COMMENT '服务名称' ,
    version_id VARCHAR(255)    COMMENT '版本ID' ,
    version VARCHAR(255)    COMMENT '版本号' ,
    status INT   DEFAULT 1 COMMENT '用例状态' ,
    pass_rate DECIMAL(24,6)    COMMENT 'PASS率' ,
    pass_count INT    COMMENT 'PASS计数' ,
    fail_rate DECIMAL(24,6)    COMMENT 'FAIL率' ,
    fail_count INT    COMMENT 'FAIL计数' ,
    run_count INT    COMMENT '执行次数' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_BY VARCHAR(32)    COMMENT '更新人' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id,name)
)  COMMENT = '测试用例' engine = innodb default charset = utf8;

DROP TABLE IF EXISTS tc_step;
CREATE TABLE tc_step(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '测试用例详情ID' ,
    tc_id INT NOT NULL   COMMENT '测试用例ID' ,
    step_order  INT NOT NULL   COMMENT '步骤顺序' ,
    step_name VARCHAR(255) NOT NULL   COMMENT '步骤名称' ,
    step_type VARCHAR(255) NOT NULL   COMMENT '步骤类型: http/python' ,
    request_id INT NOT NULL   COMMENT '请求的接口ID' ,
    request_header VARCHAR(255)    COMMENT '请求头' ,
    request_params VARCHAR(2048)    COMMENT '请求参数' ,
    assert_code VARCHAR(255)    COMMENT '断言CODE' ,
    assert_text VARCHAR(255)    COMMENT '断言文本' ,
    expression VARCHAR(255)    COMMENT '提取表达式' ,
    upload_path VARCHAR(255)    COMMENT '上传文件路径' ,
    download_path VARCHAR(255)    COMMENT '下载文件路径' ,
    database_name VARCHAR(255)    COMMENT '数据库名称' ,
    request_pick VARCHAR(255)    COMMENT '请求报文提取' ,
    database_assert_text VARCHAR(255)    COMMENT '数据库断言报文' ,
    rollback VARCHAR(255)    COMMENT '数据回滚' ,
    comments VARCHAR(255)    COMMENT '备注' ,
    CREATED_BY VARCHAR(32)    COMMENT '创建人' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_BY VARCHAR(32)    COMMENT '更新人' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id,tc_id)
)  COMMENT = '测试用例详情' engine = innodb default charset = utf8;

DROP TABLE IF EXISTS tc_api;
CREATE TABLE tc_api(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '接口ID' ,
    uri VARCHAR(255)    COMMENT '接口URI' ,
    method VARCHAR(255)    COMMENT '请求方法' ,
    description VARCHAR(255)    COMMENT '描述' ,
    module_id INT   COMMENT '模块ID' ,
    module_name VARCHAR(255)   COMMENT '模块名称' ,
    service_id VARCHAR(32)    COMMENT '服务ID' ,
    service_name VARCHAR(255)    COMMENT '服务名称' ,
    version_id VARCHAR(255)    COMMENT '版本ID' ,
    version VARCHAR(255)    COMMENT '版本号' ,
    ext VARCHAR(255)    COMMENT '扩展信息' ,
    CREATED_BY VARCHAR(32)    COMMENT '创建人' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_BY VARCHAR(32)    COMMENT '更新人' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
)  COMMENT = '测试接口' engine = innodb default charset = utf8;

DROP TABLE IF EXISTS tc_method;
CREATE TABLE tc_method(
    id INT NOT NULL AUTO_INCREMENT  COMMENT 'ID' ,
    method_name VARCHAR(32) NOT NULL   COMMENT 'Python方法名' ,
    description VARCHAR(255)    COMMENT '描述' ,
    method_ext VARCHAR(255)    COMMENT '方法扩展' ,
    module_id INT   COMMENT '模块ID' ,
    module_name VARCHAR(255)   COMMENT '模块名称' ,
    service_id VARCHAR(32)    COMMENT '服务ID' ,
    service_name VARCHAR(255)    COMMENT '服务名称' ,
    version_id VARCHAR(255)    COMMENT '版本ID' ,
    version VARCHAR(255)    COMMENT '版本号' ,
    CREATED_BY VARCHAR(32)    COMMENT '创建人' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_BY VARCHAR(32)    COMMENT '更新人' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
)  COMMENT = 'Python测试方法' engine = innodb default charset = utf8;

DROP TABLE IF EXISTS test_plan;
CREATE TABLE test_plan(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '测试计划ID' ,
    name VARCHAR(255)    COMMENT '测试计划名称' ,
    status VARCHAR(255)    COMMENT '测试计划状态' ,
    type VARCHAR(255)    COMMENT '测试计划类型' ,
    plan_ext VARCHAR(32)    COMMENT '测试计划扩展信息' ,
    comment VARCHAR(32)    COMMENT '备注' ,
    CREATED_BY VARCHAR(32)    COMMENT '创建人' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_BY VARCHAR(32)    COMMENT '更新人' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
)  COMMENT = '测试计划' engine = innodb default charset = utf8;

DROP TABLE IF EXISTS test_plan_detail;
CREATE TABLE test_plan_detail(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
    tp_id INT NOT NULL   COMMENT '测试计划ID' ,
    tc_id INT NOT NULL   COMMENT '测试用例ID' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_BY VARCHAR(32)    COMMENT '更新人' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
)  COMMENT = '测试计划详情' engine = innodb default charset = utf8;

DROP TABLE IF EXISTS test_run;
CREATE TABLE test_run(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
    tp_id INT NOT NULL   COMMENT '' ,
    CREATED_BY VARCHAR(32)    COMMENT '创建人' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_BY VARCHAR(32)    COMMENT '更新人' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = '测试执行' engine = innodb default charset = utf8;

DROP TABLE IF EXISTS test_run_record;
CREATE TABLE test_run_record(
    id INT NOT NULL AUTO_INCREMENT  COMMENT '' ,
    tr_id INT NOT NULL   COMMENT '测试执行ID' ,
    tc_id VARCHAR(255) NOT NULL   COMMENT '测试用例ID' ,
    result VARCHAR(255) NOT NULL   COMMENT '断言结果' ,
    uri VARCHAR(255)    COMMENT 'HTTP接口/Python方法' ,
    method VARCHAR(255)    COMMENT 'HTTP请求方法' ,
    request_content VARCHAR(255)    COMMENT '请求报文' ,
    response_time VARCHAR(255)    COMMENT '响应时间' ,
    response_code VARCHAR(255)    COMMENT '响应状态码' ,
    response_content VARCHAR(255)    COMMENT '响应报文' ,
    CREATED_BY VARCHAR(32)    COMMENT '创建人' ,
    CREATED_TIME DATETIME    COMMENT '创建时间' ,
    UPDATED_BY VARCHAR(32)    COMMENT '更新人' ,
    UPDATED_TIME DATETIME    COMMENT '更新时间' ,
    PRIMARY KEY (id)
)  COMMENT = '测试执行记录' engine = innodb default charset = utf8;


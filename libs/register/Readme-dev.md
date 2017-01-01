### 说明:
    只把基础实体生成的数据, 保存在mongodb中, 供二级三级实体的引用.
    因为实体之间的调用, 所以注意它们的执行顺序.

### 易错:
    testdata.DependentCallable的使用, 传入列表的名称与对应的函数参数一定要相同.
    如: add_date = DependentCallable(late_create_add_user, ['add_user_id'])
    则: late_create_add_user 必须有 参数 add_user_id.

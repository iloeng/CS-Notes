[toc]

## Database

### Intro -- 业务场景

* [从零开始深入理解存储引擎](https://mp.weixin.qq.com/s/sEml0lH2Zj-b_sIFRn2wzQ) TODO
* Data Analytics
  * 图右sql来自tpc-h


![image-20250525014902754](./Database/image-20250525014902754.png)

### mysql

没学过db。。。极速入门满足日常简单需求

https://www.runoob.com/sql/sql-tutorial.html

https://www.w3schools.com/sql/default.asp

```mysql
CREATE TABLE Persons (
    Personid int NOT NULL AUTO_INCREMENT,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    PRIMARY KEY (Personid)
);
```

* FOREIGN KEY
  * 外键 (Foreign Key) 是一个用于建立和加强两个表数据之间连接的一列或多列。它是一个表中的字段，其值必须在另一个表的主键 (Primary Key) 中存在。
  * 核心作用是保证数据的**引用完整性 (Referential Integrity)**。如果把被引用的表（包含主键）看作“父表”，把引用外部主键的表看作“子表”，那么外键约束确保了：
    * 子表中不能插入父表中不存在的外键值。
    * 不能删除父表中仍被子表引用的记录（除非定义了级联操作如 `ON DELETE CASCADE`）。
  * 外键是 `JOIN` 操作的逻辑基础，通过它可以在多个表之间查询相关数据。

```mysql
-- 接着上面的 Persons 表，创建一个 Orders 表
-- Orders 表中的 PersonID 列是外键，引用 Persons 表的 Personid 主键
CREATE TABLE Orders (
    OrderID int NOT NULL AUTO_INCREMENT,
    OrderNumber int NOT NULL,
    PersonID int,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (PersonID) REFERENCES Persons(Personid)
);
```

* NOT NULL
  * [为什么数据库字段要使用 NOT NULL？](https://mp.weixin.qq.com/s/XyOU6dimeZNjzIYyTv_fPA)

* AUTO INCREMENT



* SELECT
  * max, min, avg
  * GROUP BY
    * [not a group by expression error](https://learnsql.com/blog/not-a-group-by-expression-error/)

```mysql
# 判断范围
select min(record_id),max(record_id) from service_status where service_type='abc' limit 10;
# 精确查询规模
explain select * from  service_status where service_type='abc' and (record_id between 1 and 100000) 
# 从后往前
select * from service_status order by id desc
# 不等于
<>
# 非空
is NOT NULL
```

e.g.

```mysql
SELECT log.uid, info.source, log.action, sum(log.action), COUNT(1) AS count
FROM info, log
WHERE (log.time in LAST_7D) 
    and (log.id = info.id) 
    and (log.action=show)
GROUP by log.uid, info.source
ORDER by log.uid, info.source DESC
LIMIT 1000
```

* WITH AS
* JOIN
  * https://stackoverflow.com/questions/354070/sql-join-where-clause-vs-on-clause

```mysql
with temp as(
	select a,b,c
  where a=.. AND b=.. AND c=..
)
select A.a
from temp A join temp B
on A.a = B.a
group by A.a
```

```mysql
# 高级 JOIN 技巧
# Using the Same Table Twice
SELECT a.account_id, e.emp_id, b_a.name open_branch, b_e.name emp_branch 
FROM account AS a 
INNER JOIN branch AS b_a ON a.open_branch_id = b_a.branch_id 
INNER JOIN employee AS e ON a.open_emp_id = e.emp_id 
INNER JOIN branch b_e ON e.assigned_branch_id = b_e.branch_id WHERE a.product_cd = 'CHK';

# Self-Joins
SELECT e.fname, e.lname, e_mgr.fname mgr_fname, e_mgr.lname mgr_lname
FROM employee AS e INNER JOIN employee AS e_mgr
ON e.superior_emp_id = e_mgr.emp_id;

# Non-Equi-Joins
SELECT e1.fname, e1.lname, 'VS' vs, e2.fname, e2.lname
FROM employee AS e1 INNER JOIN employee AS e2
ON e1.emp_id < e2.emp_id WHERE e1.title = 'Teller' AND e2.title = 'Teller';
```

* OVER PARTITON BY
  * https://learnsql.com/blog/partition-by-with-over-sql/

```mysql
SELECT
    car_make,
    car_model,
    car_price,
    AVG(car_price) OVER() AS "overall average price",
    AVG(car_price) OVER (PARTITION BY car_type) AS "car type average price"
FROM car_list_prices
```

```mysql
WITH year_month_data AS (
  SELECT DISTINCT
       EXTRACT(YEAR FROM scheduled_departure) AS year,
       EXTRACT(MONTH FROM scheduled_departure) AS month,
       SUM(number_of_passengers)
              OVER (PARTITION BY EXTRACT(YEAR FROM scheduled_departure),
                                  EXTRACT(MONTH FROM scheduled_departure)
                   ) AS passengers
   FROM  paris_london_flights
  ORDER BY 1, 2
)
SELECT  year,
        month,
     passengers,
     LAG(passengers) OVER (ORDER BY year, month) passengers_previous_month,
     passengers - LAG(passengers) OVER (ORDER BY year, month) AS passengers_delta
FROM year_month_data;
```

```mysql
AVG(month_delay) OVER (PARTITION BY aircraft_model, year
                               ORDER BY month
                               ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
                           ) AS rolling_average_last_4_months
```

* ALTER TABLE

```mysql
ALTER TABLE
  service_status
ADD
  error_count_avg decimal(10, 5) NOT NULL DEFAULT 0 COMMENT "服务错误量",
MODIFY
  error_code int(11) NOT NULL COMMENT "请求错误类型（取最多的）",
MODIFY
  is_error int(5) NOT NULL COMMENT "是否是错误请求";
  
ALTER TABLE test TABLE (c1 char(1),c2 char(1));
```



* TIMESTAMP

```mysql
`record_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录产生时间'
```



* [SQL Injection 注入攻击](https://www.w3schools.com/sql/sql_injection.asp)
  * SQL Injection Based on 1=1 is Always True
  * SQL Injection Based on ""="" is Always True
  * SQL Injection Based on Batched SQL Statements
    * 在输入中用分号分隔语句
  * Use SQL Parameters for Protection



#### 函数

* Count、Sum
  * count是行数、sum是求和
* `log(greatest(val,1e-6))`



### db client

#### Redis 常见接口

- put
- get key or keys
- mget
  - Input: keys
  - Output: indices, results
- hset
  - e.g. Redis: https://redis.io/docs/reference/optimization/memory-optimization/#use-hashes-when-possible
  - 存储结构化数据
- remove key or keys
- zcard
  - Returns the sorted set cardinality (number of elements) of the sorted set stored at `key`.
- zremrangebyscore(key, start, end)
  - Removes all elements in the sorted set stored at `key` with a score between `min` and `max` (inclusive).
- sadd、zadd、hset
  - sadd：set
  - zadd：sorted set (element with score)
  - hset：https://redis.io/commands/hset/

### 数据库优化

#### Dictionary Encoding

#### 同时支持 Query 和 Span

* scan：底层存储连续
* query：设计计算缓存层





### 图数据库

#### Gremlin

https://tinkerpop.apache.org/docs/current/reference/#_tinkerpop_documentation

* 建模细节：
  * 对边类型做拆分
  * 边索引：`g.V(A).outE('follow').order().by('age')`
* 基础命令
  * path
  * by
    * 作为Path修饰器，对Path上的元素Element执行投影计算。

```
g.V().has('id', {CityHash32(c)}).has('type', 2).outE('Company2Person').otherV().inE('Company2Person').otherV().outE('Company2Person').otherV().has('type', 1).has('id', {CityHash32(p)}).path().by(properties('name')).by(properties('role'))
```

* 规范
  * 判断点存在性：不能使用g.V().has("id", xxx).has("type", yyy)。原因是点有2种语义分别是属性点和边的端点。
    * 判断属性点存在性： 使用g.V().has("id", xxx).has("type", yyy).properties() 如果返回空，表示不存在。
    * 判断边端点存在性： 使用g.V().has("id",xxx).has("type",yyy).outE(edge_type).count()，如果返回0，表示不存在。
  * 新增(addV)或修改点(Property(key, value))，需要进行点存在性判断。
    * 添加点(addV)是覆盖语义，会把已有的点删除，再重新写入，导致原有的数据丢失。
    * 修改点(Property) 只能修改已存在点，不能新建属性，否则会报错。
  * 使用drop删除addV产生的点，删除点的属性，点并没有真正删除，只能由底层存储进行compact，降低空间占用。
  * 点的update-or-insert不支持原子性，边的update-or-insert并发下只能保证1个记录成功，其他会失败。 如有强需求使用原子性, 建议业务层实现。

```
g.V().has("id",A.id).has("type",A.type)
 .property("age", 28) // 如果A点存在，更新点的属性
 .fold()              // 结果为[]或[Vertex(A)]
 .coalesce(unfold(),  // 如果是[Vertex(A)],直接返回
   g.addV().overwrite(false).property("id",A.id).property("type",A.type)
    .property("age", 28) // 如果是[]，插入A并更新属性
  )              // coalesce 返回结果一定是 Vertex(A)
```

* 多跳查询：
  * 例如1跳出度为n，二跳出度为m。第1跳查询的次数为1，出现记录数为n，第2跳查询次数为n，输出记录为m，所以共需要查询次数为n+1，遍历总记录数为n*m。
* 技巧：
  * 引入虚拟点：
    * A->B
    * A->C
      * 点C的属性：B上要维护的属性
      * 边A->C的属性：B.id、B.type

* 例子：

```
# 插入一条 (1,1) -> (2,1) 的正向边
g.V().addE('follow').from(1,1).to(2,1).property('tsUs', 123)
# 从 (2,1) 出发，做入度查询，也就是反向查询
g.V(vertex(2,1)).inE('follow').count()

# 双向边
g.V(vertex(2,1)).double('follow').count()
```



```
# 关注
g.addE("follow").from(100, 2).to(200, 2).setProperty("tsUs", 1234).setProperty("closeness", 20)
# 取关
g.V(vertex(100, 2)).outE("follow").where(otherV().has("id", 200).has("type", 2)).drop()
# 按关注时间排序
g.V(vertex(100, 2)).outE("follow").order().by("tsUs").limit(10).otherV()
# 判断关系
g.V(vertex(100, 2)).outE("follow").where(otherV().has("id", 200).has("type", 2))
# 粉丝数量
g.V(vertex(100, 2)).in("follow").count()

# 使用local，子查询
g.V(vertex(100, 2)).out("follow").local(out("like").limit(100))
g.V(vertex(100, 2)).out("follow").out("follow").local(in("follow").count().is(le(500)))

# 按边属性筛选点
g.V(vertex(100, 2)).outE("follow").has("closeness", 20).otherV()

# 同时关注
g.V().has("id", C.id).has("type", C.type)
 .out("follow")
 .store("vertices")
 .count()
 .local(
        g.V().has("id", A.id).has("type", A.type)
         .out("follow")
         .where(P.within("vertices")))

# A->C路径
.g.V().has("id", A.id).has("type", A.type)
 .repeat(                              // repeat()表示表示迭代从A找关注or被关注的人
        both("follow")
        .simplePath())                 // simplePath()是过滤条件，出现环则过滤掉
 .until(                               // until()指定repeat步骤的终止条件是:
        or(has("id", C.id).has("type", C.type),  // 1. 找到了用户C，或者
           loops().is(gte(4))))                  // 2. 找了4度还没有找到；
 .emit(has("id", C.id).has("type", C.type))  // emit()表示只保留遍历终点是C的结果
 .path()                                     // path()表示生成起点A到终点C的路径
```





### 数据一致性

* 多版本并发控制(Multiversion concurrency control, MCC 或 **MVCC**)
  * 是数据库管理系统常用的一种并发控制，也用于程序设计语言实现事务内存。MVCC意图解决读写锁造成的多个、长时间的读操作饿死写操作问题。每个事务读到的数据项都是一个历史快照（snapshot)并依赖于实现的隔离级别。写操作不覆盖已有数据项，而是创建一个新的版本，直至所在操作提交时才变为可见。快照隔离使得事物看到它启动时的数据状态



### Hive

* hadoop 生态下的OLAP引擎，将 SQL 查询翻译为 map reduce 任务，特点是稳定，成功率高，但是查询速度慢

* API v.s. mysql

  * `percentile(a, array(0.5,0.9,0.99))` 求分位数（mysql没有这个函数）
  * [Hive Aggregate Functions](http://hadooptutorial.info/hive-aggregate-functions/)

* 用 Spark 做 mysql to Hive 的同步

  * ```
    spark.mysql.remain_delete = true
    ```

* 细节
  * p_date和p_hour是hive分区字段

### MongoDB

MongoDB是文档型、无强制 schema 的存储；单条读取时只返回“实际存储在该文档里的键”。即便某字段在你的业务“定义了默认值”，只要没写进该文档，就不会在查询结果里自动出现任何“默认值”。这是数据库层面的行为。

#### Aggregation Framework

MongoDB 的聚合框架是处理和转换文档集合的强大工具。它通过一个由多个阶段（stage）组成的管道（pipeline）来处理数据。每个阶段对输入的文档进行操作，并将结果传递给下一个阶段。

这对于数据分析和特征工程非常有用。

**常用阶段 (Stages):**

*   `$match`: 过滤文档，类似于 `find()` 查询。通常放在管道的开头以减少后续处理的数据量。
*   `$project`: 重塑文档，可以指定包含/排除字段，或使用表达式创建新字段。
*   `$group`: 按指定的键对文档进行分组，并对每个组应用累加器表达式（如 `$sum`, `$avg`, `$addToSet`）。
*   `$sort`: 对文档进行排序。
*   `$limit`: 限制输出的文档数量。
*   `$unwind`: 将数组字段中的每个元素拆分为一个独立的文档。

**示例：使用聚合管道进行分布式计算**

以下示例展示了如何使用聚合管道计算每个用户的唯一物品交互次数，并支持分布式计算。

```json
// 假设集合中的文档结构为 { user_id: "...", item_id: "...", timestamp: ... }
[
  // 阶段 1: (可选) 按时间范围过滤
  {
    "$match": { "timestamp": { "$gte": 1672531200, "$lt": 1675209600 } }
  },
  // 阶段 2: 按 user_id 分区，用于分布式计算
  // 通过对 user_id 的哈希值取模，可以将数据分散到不同的 worker
  {
    "$match": {
      "$expr": {
        "$eq": [
          { "$mod": [{ "$toLong": { "$toHashedIndexKey": { "field": "$user_id" } } }, 4] }, // world_size = 4
          0 // rank = 0
        ]
      }
    }
  },
  // 阶段 3: 按 user_id 分组，并收集不重复的 item_id
  {
    "$group": {
      "_id": "$user_id",
      "unique_items": { "$addToSet": "$item_id" }
    }
  },
  // 阶段 4: 计算唯一物品的数量
  {
    "$addFields": {
      "unique_item_count": { "$size": "$unique_items" }
    }
  },
  // 阶段 5: 整理输出
  {
    "$project": {
      "user_id": "$_id",
      "unique_item_count": 1,
      "_id": 0
    }
  }
]
```

**关键技巧:**

*   **分布式计算/分区**: 使用 `$toHashedIndexKey` 将字符串字段转换为64位哈希值，然后通过 `$mod` 运算符实现数据分区，以便在多个 worker 上并行处理。`$bitAnd` 与 `0x7FFFFFFFFFFFFFFF` 一起使用可以确保结果为正数。
*   **处理大数据集**: 在执行聚合时，设置 `allowDiskUse=True` 允许 MongoDB 在内存不足时使用磁盘空间，这对于大型数据集至关重要。
*   **游标设置**: 对于可能长时间运行的查询，设置 `no_cursor_timeout=True` 可以防止游标因超时而关闭。

#### 并行分片：rank/world_size 模式

- 目标：在 `world_size` 个 worker 上均匀切分集合，保证每个文档只被一个 worker 处理。
- 分片规则：对稳定键 \(k\) 的 64 位哈希取模，将文档分配到第 \(r\) 个 worker：
  - $$ r = \mathrm{mod}(\mathrm{hash}(k),\ \text{world\_size}) $$
  - 拉取满足：$$ \mathrm{mod}(\mathrm{hash}(k),\ \text{world\_size}) = \text{rank} $$
- Mongo 实现：
  - 若已预存数值型哈希键 `hash_k`：
    - `{"$expr": {"$eq": [{"$mod": ["$hash_k", world_size]}, rank]}}`
  - 若未预存：用 `$toHashedIndexKey` + `$toLong` 现场计算哈希并取模：
    - `{"$expr": {"$eq": [{"$mod": [{"$toLong": {"$toHashedIndexKey": {"field": "$k"}}}, world_size]}, rank]}}`
  - 时间过滤：
    - `{"_event_date": {"exists": true, "$gte": start, "$lt": end}}`（仅给定一端则保留相应约束）；`exists` 可用于清洗脏数据。
- 输出文件防冲突：分布式写本地文件时，文件名附加 `_{rank}` 后缀（如 `items_3.tsv`）。
- 游标与资源：设置 `allowDiskUse=True`、`batch_size(1024)`、`no_cursor_timeout=True`、`maxTimeMS` 以适配长任务。
- 正确性要点：
  - 选用稳定哈希函数，保证跨 worker 分片一致；所有 worker 使用相同的 `world_size`，并校验 `rank < world_size`。
  - 分片键应与业务唯一键一致（如 `item_id`/`user_id`），减少倾斜与重复处理。

参考：[`$expr`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/expr/)、[`$mod`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/mod/)、[`$toHashedIndexKey`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/toHashedIndexKey/)

#### Sharding (分片架构)

Sharding 是 MongoDB 将数据分布到多台机器上的方法，用于支持大数据集和高吞吐量操作。一个分片集群（sharded cluster）主要由以下组件构成：

*   **Shards (分片)**: 每个分片存储了总数据的一个子集。分片本身可以是一个副本集（replica set），以保证高可用。
    *   **Shards规格**: 指的是每个分片服务器的硬件配置，例如 CPU核心数、内存大小。这是数据存储和处理的主要资源。
*   **Mongos (查询路由)**: 这是一个路由服务，负责将客户端的查询和写入操作转发到正确的分片上。客户端直接与 `mongos` 交互，而不是直接连接到分片。`mongos` 本身不存储数据，是无状态的。
    *   **Mongos节点规格**: 指的是 `mongos` 服务器的硬件配置。由于其无状态的路由特性，其资源需求（特别是磁盘）通常低于分片服务器。
*   **Config Servers (配置服务器)**: 存储了集群的元数据（metadata）和配置信息，例如数据在各个分片上的分布情况。配置服务器也必须是副本集。

#### Time Series Collections

Time Series 集合是 MongoDB 专门为处理时间序列数据（如日志、物联网传感器数据）设计的，它通过将数据组织到内部的 bucket 中来优化存储和查询性能。

##### 核心查询优化

- **索引与 Bucket 剪枝**
  - **metaField 索引**: 查询应优先利用在 `metaField` 上创建的索引（如 `_meta_data._user_id`）。优化器可在“解包” bucket 前就利用该索引过滤掉大量不相关的 buckets，这是提升性能的关键。
  - **时间窗口过滤**: 时间范围的 `$match` 必须尽量在 bucket 级别表达。这意味着查询条件需要让优化器能够利用 `control.min.<timeField>` 和 `control.max.<timeField>` 这两个 bucket 级别的元数据来快速排除不相关的 buckets（即“剪枝”）。
    - **工作原理**: 将 `timeField` 的范围查询作为聚合管道的第一个 `$match` 阶段，优化器会自动利用 `system.buckets.*` 集合上关于 `control.min/max` 的内置索引，在解包数据前就完成大部分筛选。
    - **反面教材**: 如果时间过滤被放在 `$project` 之后，或在 `eventFilter` 中，或用复杂的 `$expr` 表达式，优化器将无法进行 bucket 剪枝，导致性能急剧下降（退化为全表扫描或大范围索引扫描）。
    - **验证方法**: 通过 `explain()` 查看执行计划，确认是否有效利用了 `TS_BUCKET_SCAN` 等阶段，并观察 `nReturned`（返回的 bucket 数量）是否远小于总数。

- **查询管线与顺序**
  - **推荐顺序**:
    1.  `$match`: 仅保留可高效命中索引的条件，如 `metaField` 字段、时间窗口。
    2.  `$_internalUnpackBucket`: MongoDB 内部阶段，用于解包 bucket。
    3.  `$project`: 统一字段命名，为后续阶段做准备。
    4.  `$match`: 对解包后的数据进行二次过滤，如 `$exists: true` 或 `$ne: null` 等低选择性条件。
    5.  `$sort` / `$group`: 在数据量已显著减少后执行这些聚合操作。
  - **经验法则**: 避免将 `$exists` 或 `$ne: null` 等无法有效利用索引的条件放在管道的最前端，这会干扰查询优化器选择最佳索引。应将这类存在性校验后置。

##### 诊断与分析

- **慢查询日志 (`planSummary`)**
  - 检查 `planSummary` 中是否包含对 `metaField` 或 `control.min/max` 的过滤。如果只看到 `IXSCAN`（没有命中用户定义的 `metaField` 索引）或 `COLLSCAN`，说明查询性能不佳。

- **Explain Plan**
  - 使用 `db.collection.explain().aggregate(...)` 来分析聚合管道的执行计划，确认是否命中了预期索引。

- **Hint 使用**
  - 在某些情况下，可以通过 `hint()` 来强制查询优化器使用特定的索引，以保证查询路径的稳定性。例如：`aggregate(..., hint='my_timeseries_index')`。

### 特征工程

[滴滴特征工程](https://mp.weixin.qq.com/s/vUP4LAA7gAYDo91Wd5rSQQ)


### OLAP

DSL like ES -> (forward/aggregation/post-aggregation) -> view -> physical table

* 难点是异构数据源查询，使用 query engine 封装收口了所有 olap 引擎的查询，同时用服务聚合多数据源数据，格式化&聚合 后返回给用户，带来的挑战是研发同学需要熟悉各个数据源特性时延精确去重，异构数据源聚合等
* 指标杂乱，一张物理表几万个指标，配置分散在上十个元文件中
* [浅谈数据治理、数据管理、数据资源与数据资产管理内涵及差异点](https://mp.weixin.qq.com/s/B9t1ZdNEl8u0mhxDLyS8-A)

* [滴滴指标体系](https://mp.weixin.qq.com/s/-pLpLD_HMiasyyRxo5oTRQ)

### 论文

#### Spitfire: A Three-Tier Buffer Manager for Volatile and Non-Volatile Memory, SIGMOD 2021

介绍视频：https://www.bilibili.com/video/BV1164y1d7HD

![image-20210808000446554](Database/hymem.png)

![dram-nvm-ssd](Database/dram-nvm-ssd.png)




nvm读写性能介于dram和ssd之间，更接近dram

2.Hymem

* 对比Spitfire：Hymem是single-threaded，且是NVM-aware的，对emulation有依赖
* clock algo逐出nvm、ssd
* the cache line-grained loading and mini-page optimizations must be tailored for a real NVM device. We also illustrate that the choice of the data migration policy is significantly more important than these auxiliary optimizations.
* 行为
  * DRAM admission: 如果没在DRAM中找到，eagerly SSD->DRAM，跳过 SSD->NVM
  * DRAM eviction: 用是否在 recent queue 中决定是否进 nvm
  * cache-line-grained page (256 cache lines): resident + dirty bitmap; 指向nvm page的指针
  * mini page (<16 cache lines): dirty bitmap + slots; count; full page

3.NVM-Aware Data Migration

* 目标：利用NVM提供的数据新通路，minimize the performance impact of NVM and to extend the lifetime of the NVM and SSD devices
  * lazy data migration from NVM to DRAM ensures that only hot data is promoted to DRAM.
  * 延续CLOCK策略，引入概率插入来决定migrate到哪一层存储
* 实现策略
  * Bypass DRAM during reads
    * lazily migrate data from NVM to DRAM
      while serving read operations.
    * ensures that warm pages on NVM do not evict hot pages in DRAM
  * bypass DRAM during writes
    * DBMSs use the group commit optimization to reduce this I/O overhead [9]. The DBMS first batches the log records for a group of transactions in the DRAM buffer (❹) and then flushes them together with a single write to SSD
    * Dw，减少hot pages在DRAM上的eviction
  * Bypass NVM during reads
    * a lazy policy for migrating data from NVM to DRAM (Dr = 0.01), and a comparatively eager policy while moving data from SSD to NVM (Nr = 0.2). While this scheme increases the number of writes to NVM compared to the lazy policy, it enables Spitfire to deliver higher performance than Hymem (§6.5)
    * This design reduces data duplication in the NVM buffer.
  * Bypass NVM during writes
    * 不同于hymem用recent queue，spitfire用随机插入来决定进入nvm的页

4.Adaptive Data Migration

* 相关论文：On multi-level exclusive caching: offline optimality and why promotions are better than demotions, FAST 2008
* 用模拟退火来搜索参数

5.System Architecture

5.1 Multi-Tier Buffer Management

* When a page is requested, Spitfire performs a table lookup that returns a shared page descriptor containing the locations (if any) of the logical page in the DRAM and NVM buffers.

* 数据结构：
  * {page_index -> shared_page_descriptor}
    * shared_page_descriptor: {latch_dram, latch_nvm, latch_ssd, dram_pd, nvm_pd}
      * dram_pd: {num_of_users, is_dirty, physical_pointer}

5.2 Concurrency Control and Recovery

* To support concurrent operations, we leverage the following data structures and protocols:
  * a concurrent hash table for managing the mapping from logical page identifiers to shared page descriptors [17]
  * a concurrent bitmap for the cache replacement policy [40]
  * multi-versioned timestamp-ordering (MVTO) concurrency control protocol [39]
  * concurrent B+Tree for indexing with optimistic lock-coupling [24]
  * lightweight latches for thread-safe page migrations
    * [数据库中 lock 和 latch 的区别](https://www.zhihu.com/question/309342903/answer/1699205097)

6.Experimental Evaluation

6.1 workload

* YCSB: Zipfian Distribution
* TPC-C

6.2 Benefits of NVM and App-Direct Mode

* memory-mode requires an upfront NVM capacity at least equal to the size of DRAM. In contrast, with app-direct mode, it could give a higher buffer capacity due to its cost advantage, though the NVM is bit slower. This is especially useful with a large working set.
* with app-direct mode, Spitfire exploits the persistence property of NVM to reduce the overhead of recovery protocol by eliminating the need to flush modified pages in NVM buffer.

6.3 Data Migration Policies

* With eager policies, more pages are updated in DRAM, and they must be flushed down to lower tiers of the storage system (even when the update is localized to a small chunk of the page). In contrast, with a lazy scheme, Spitfire updates page in NVM, thereby reducing write amplification.
* impact of storage hierarchy
  * DRAM/NVM的比例越大，migration probability对吞吐的影响越大。假如DRAM非常小，with the eager policy, the performance improvement brought by adding the comparatively smaller DRAM buffer (1.25 GB) is shadowed by the cost of data migration between DRAM and NVM

6.5 Revisiting Hymem’s Optimizations

* We attribute the 1.1× lower throughput at 64 B granularity (relative to 256B granularity) to the I/O amplification stemming from the mismatch between the device-level block size and loading granularity.

6.6 Storage System Design

* 指标：performance/price numbers

* insights	
  * To achieve the highest absolute performance, the hierarchy usually consists of DRAM (since DRAM has the lowest latency).
  * If the workload is read-intensive, DRAM-NVM-SSD hierarchy is the best choice from a performance/price standpoint, since it is able to ensure the hottest data resides in DRAM.
  * If the workload is write-intensive, NVM-SSD hierarchy is the best choice from a performance/price standpoint, since NVM is able to reduce the recovery protocol overhead.




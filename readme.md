﻿Python爬取Steam游戏评论 + 游戏基本信息用于数据分析练习。

爬取数据结构：

```
- PySteam
	- GameName-GameSteamID
		- Source
			- GameName-GameSteamID-Review.json
			- GameName-GameSteamID-Summary.html
			- GameName-GameSteamID-Summary.json
		- GameName-GameSteamID-review_post.csv
		- GameName-GameSteamID-review_sus_post.csv #隔离无效评论
		- GameName-GameSteamID-summary_post.csv
		- GameName-GameSteamID-achievements_post.csv
		- GameName-GameSteamID-wordcloud_post #评论词数统计
		- wordcloud.png #评论总词云图
		- wordcloud_n.png #评论名词词云图
		- wordcloud_zn.png #评论专名词云图
		- wordcloud_v.png #评论动词词云图
		- wordcloud_t.png #评论状语词云图
		- wordcloud_adj.png #评论形容词词云图

# GameName-GameSteamID-review_post.csv
	steamid #用户ID
	num_games_owned #用户账户游戏数
	num_reviews #用户账户评论数
	playtime_forever(min) #用户总游戏时长
	playtime_last_two_weeks(min) #用户过去两周游戏时长
	playtime_at_review(min) #用户评论时游戏时长
	last_played #用户上次进入游戏时间

	recommendationid #评论唯一ID
	language #评论语言
	review #评论内容
	timestamp_created #评论创建日期
	timestamp_updated #评论更新日期
	voted_up #是否推荐

	votes_up #点赞数
	votes_funny #觉得有趣数
	weighted_vote_score #评论影响权重
	comment_count #子评论数
	steam_purchase #是否于Steam购买
	received_for_free #是否免费获取
	written_during_early_access #是否于抢先体验期间撰写评论
	review_length #评论长度(字符)
	review_updated #评论是否更新过
	timestamp_dev_responded #开发者回复日期
	developer_response #开发者回复

# GameName-GameSteamID-achievements_post.csv
	index #序号
	achievement_name #成就名称
	achievement_desc #成就描述
	achievement_percentage #全球成就达成百分比

# GameName-GameSteamID-summary_post.csv
	name #游戏名
	developer #开发商
	publisher #发行商
	desc #游戏介绍
	date #游戏发行日期
	tags #游戏标签
	price #价格
	review_total #整体评价情况
	review_recent #最近30天评价情况
	steam_feature #Steam功能支持
	achievement_num #成就数
	support_languages #语种支持
	Support_Sch #是否支持简中
	language_num #语种支持数量
	num_reviews #review_post.csv 中获取的评论数
	review_score  #整体评价分数(1-9)
	review_score_desc  #整体评价分数描述
	total_positive  #（符合筛选条件的）推荐评价数
	total_positive  #（符合筛选条件的）不推荐评价数
	total_reviews #（符合筛选条件的）评价总数
	filter #筛选条件：排序（详情见源程序内设置）
	language #筛选条件：评论语言（详情见源程序内设置）
	day_range #筛选条件：日期范围（详情见源程序内设置）
	review_type #筛选条件：评测是否推荐（详情见源程序内设置）
	purchase_type #筛选条件：是否Steam购买（详情见源程序内设置）

# GameName-GameSteamID-review_sus_post.csv
	同GameName-GameSteamID-review.csv

# GameName-GameSteamID-wordcloud_post
	word  #词
	count  #出现次数

```


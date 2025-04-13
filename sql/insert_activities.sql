-- 插入 10 条活动数据 (更新图片路径并生成唯一的简化 slug)
INSERT INTO `activities_activity` (`title`, `slug`, `description`, `start_time`, `end_time`, `location`, `category_id`, `cover_image`, `max_participants`, `farmer_id`, `created_at`, `updated_at`) VALUES
('体验采摘新鲜草莓的乐趣', 'caomei-lequ-1', '欢迎来到我们的草莓园，亲手采摘饱满多汁的草莓，享受田园时光。', '2025-05-01 10:00:00', '2025-05-01 12:00:00', '阳光草莓园', 1, 'backend/activities/covers/strawberry_picking.jpg', 30, 1, NOW(), NOW()),
('学习传统手工陶艺制作', 'shougong-taoyi-1', '跟随经验丰富的陶艺师傅，从泥土开始，亲手制作一件独一无二的陶艺作品。', '2025-05-15 14:00:00', '2025-05-15 17:00:00', '泥土艺术工作室', 1, 'backend/activities/covers/pottery_making.jpg', 20, 1, NOW(), NOW()),
('探索神秘的乡村徒步之旅', 'xiangcun-tubu-1', '沿着古老的乡村小路，穿越森林和溪流，发现隐藏的美景和宁静。', '2025-05-22 09:00:00', '2025-05-22 16:00:00', '绿野山谷', 1, 'backend/activities/covers/hiking_adventure.jpg', 15, 1, NOW(), NOW()),
('体验传统农耕文化，播种希望', 'nonggeng-wenhua-1', '参与到真实的农耕活动中，学习播种、施肥等技巧，感受劳动的快乐和收获的喜悦。', '2025-06-05 09:30:00', '2025-06-05 11:30:00', '希望田野', 1, 'backend/activities/covers/planting_crops.jpg', 40, 1, NOW(), NOW()),
('品尝地道农家菜，体验乡村美食', 'nongjia-meishi-1', '在农家小院里，品尝由新鲜食材烹制而成的地道农家菜肴，感受淳朴的乡村风味。', '2025-06-12 12:00:00', '2025-06-12 14:00:00', '老王农家小院', 1, 'backend/activities/covers/farm_to_table_lunch.jpg', 25, 1, NOW(), NOW()),
('夜观星空，聆听自然的低语', 'yeguan-xingkong-1', '远离城市的喧嚣，来到乡村，仰望璀璨的星空，聆听夜晚大自然的声音，放松身心。', '2025-06-26 20:00:00', '2025-06-26 22:00:00', '星空观测点', 1, 'backend/activities/covers/stargazing_night.jpg', 10, 1, NOW(), NOW()),
('亲手制作美味的手工面条', 'shougong-mian-1', '学习如何用传统方法制作劲道十足的手工面条，体验揉面、擀面、切面的乐趣，最后品尝自己的劳动成果。', '2025-07-03 15:00:00', '2025-07-03 17:00:00', '面条坊', 1, 'backend/activities/covers/handmade_noodles.jpg', 18, 1, NOW(), NOW()),
('体验清晨的鸟鸣和瑜伽', 'qingchen-yuming-yujia-1', '在清新的乡村早晨，伴随着鸟儿的歌唱，进行一场舒缓身心的瑜伽练习，开启美好的一天。', '2025-07-10 07:00:00', '2025-07-10 08:30:00', '静心草坪', 1, 'backend/activities/covers/morning_yoga.jpg', 22, 1, NOW(), NOW()),
('学习制作传统豆腐的全过程', 'chuantong-doufu-1', '了解豆腐的制作工艺，从黄豆到嫩滑的豆腐，亲手体验每一个环节，感受传统美食的魅力。', '2025-07-17 10:30:00', '2025-07-17 13:00:00', '豆腐坊', 1, 'backend/activities/covers/tofu_making.jpg', 28, 1, NOW(), NOW()),
('在乡村体验宁静的垂钓乐趣', 'xiangcun-chuidao-1', '在宁静的乡村池塘边，享受悠闲的垂钓时光，放松心情，感受大自然的馈赠。', '2025-07-24 16:00:00', '2025-07-24 18:00:00', '静心湖畔', 1, 'backend/activities/covers/peaceful_fishing.jpg', 12, 1, NOW(), NOW());



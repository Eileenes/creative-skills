// ======= 只需要改这个文件 =======
// 所有文字、数据都在这里；素材图片放在 public/ 目录
export const CONFIG = {
  name: 'Soren',                       // 昵称（结尾大标签）
  handle: '@Eileeness160708',          // 账号
  cta: '关注 Soren',                    // 结尾红色行动号召
  headline: 'AI 新工具测评',             // 一句话定位（拼贴墙大红标签 + 结尾标签）
  subline: '产品经理 | Vibe Coding 选手', // 拼贴墙第二行
  slogan: '测评 AI 新工具，分享真实上手体验', // 拼贴墙底部描边字
  photoTag: '1024 程序员节快乐！',        // 照片旁的小标签（可写代表作主题）
  stats: [                             // 拼贴墙三张数据卡
    {num: '395', label: '帖子', color: '#1d9bf0'},
    {num: '591', label: '粉丝', color: '#d93a2b'},
    {num: '324', label: '关注', color: '#16181c'},
  ],
  pinnedViews: 7400,                   // 置顶帖浏览量（数字滚动目标值）
  viewsUnit: '浏览',
  pinnedTag: '梁山好汉 10/108',          // 置顶帖旁的小标签
  photos: ['m1.jpg', 'm2.jpg', 'm3.jpg', 'm4.jpg'], // 拼贴墙上的 4 张帖子配图
  // 头像在 profile.png 中的中心坐标（2x 截图像素）。X 主页用默认截图参数时不用改
  avatarCenter: {x: 168, y: 504},
  // 若 public/ 里有 figure.png（抠好图的 3D 小人）设为 true；否则用头像做圆形立牌
  useFigure: false,
};

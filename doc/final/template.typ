#let colab(
  name: "实验名称",
  instructor: "教师",
  lab_name: "实验名称",
  class: "班级",
  ta: "助教",
  author: "姓名",
  author-id: "学号",
  date: datetime.today(),
  week: 1,
  am-pm: "上午",
  body
) = {
  let 小初 = 36pt
  let 三号 = 16pt
  let 四号 = 14pt
  let 小四 = 12pt
  // 设置文档元数据
  set document(title: author + "-"+ name, author: author)
  // 设置字体
  set text(font: "SimSun", size: 四号)
  show raw: set text(font: ("Consolas", "SimSun"), size: 10pt)
  // show heading.where(level: 1): set heading(numbering: "一、")
  // show heading.where(level: 1): set text(stroke: 0.03em)
    // ==== 新增：标题样式设置 ====
  // 一级标题（加粗，16pt，中文数字编号）
  show heading.where(level: 1): set heading(numbering: "一、")
  show heading.where(level: 1): set text(stroke: 0.03em, size: 三号)
  show heading.where(level: 1): set block(above: 1.5em, below: 1em)
  
  // 二级标题（加粗，15pt，括号中文数字编号）
  show heading.where(level: 2): set heading(numbering: "1.")
  show heading.where(level: 2): set text(stroke: 0.03em, size: 15pt)
  show heading.where(level: 2): set block(above: 1.2em, below: 1em)
  
  // 三级标题（加粗，14pt，阿拉伯数字编号）
  show heading.where(level: 3): set heading(numbering: "1.")
  show heading.where(level: 3): set text(stroke: 0.03em, size: 四号)
  show heading.where(level: 3): set block(above: 1em, below: 1em)
  // 四级标题（加粗，12pt，英文数字编号）
  show heading.where(level: 4): set heading(numbering: "1.")
  show heading.where(level: 4): set text(stroke: 0.03em, size: 小四)
  show heading.where(level: 4): set block(above: 0.8em, below: 0.8em)
  // ===========================
  // 设置纸张大小与页边距
  set page(paper: "a4", margin: (top: 2.54cm, bottom: 2.54cm, left: 1.91cm, right: 1.91cm), numbering: (..args) => {
    let ind = args.pos().at(0)
    if ind > 1 {
      "第" + str(args.pos().at(0) - 1) + "页" 
    }
  }
  )

  // 封面部分开始
  set align(center)
  image("assets/ZJULOGO.jpg", fit: "cover", width: 5cm)
  set text(stroke: 0.03em, size: 三号)
  set align(center)
  set box(stroke: (bottom: 1pt), inset: (bottom: 20%, left: -10%, right: -10%))
  v(0.6fr)
  text("数据可视化导论\n课程大作业\n ", size: 小初)
  v(0.1fr)
  [#text(lab_name, size:24pt)]
  v(2cm)
  [#box("教师:", stroke: none) #box(instructor, width: 9.4cm)]
  v(.1cm)
  [#box("班级:", stroke: none) #box(class, width: 9.4cm)]
  v(.1cm)

  [#box("成员:", stroke: none) #box("李文耀 3230102302", width: 9.4cm)]
  v(.1cm)
  [#box("     ", stroke: none) #box("汪昕  3230101888", width: 9.4cm)]
    v(.1cm)
  [#box("     ", stroke: none) #box("刘烨  3230105721", width: 9.4cm)]

  v(0.5fr)
  [#box("日期：", stroke: none) #box(str(date.year()), width: 3em) #box("年", stroke: none) #box(str(date.month()), width: 1.5em) #box("月", stroke: none) #box(str(date.day()), width: 1.5em) #box("日", stroke: none) #h(1cm) #box("星期", stroke: none) #box("一二三四五六日".clusters().at(date.weekday() - 1), width: 1em)]
  v(0.5fr)
  set text(stroke: none)
  set align(left)
  set text(size: 小四)
  v(1fr)
  // 封面部分结束
  pagebreak()
  body
}

#let problem-counter = counter("problem")
#problem-counter.step()

#let solution(body) = {
  set enum(numbering: "(1)")
  block(
    inset: 8pt,
    width: 100%
  )[*解答.* #h(0.75em) #body]
}
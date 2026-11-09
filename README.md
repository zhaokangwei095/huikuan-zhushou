# 回款助手 · huikuan-zhushou

帮自由职业者、个体工商户和小微商家把一单生意的钱**算清、说清、收清**
的中文 Agent Skill：报价单、简易服务合同、收款确认单、对账台账、
礼貌催款话术，一条链路一次走完。

适用人群：设计师、程序员、摄影师、装修师傅、家政、培训老师、小店老板
——所有以单接单、靠微信谈生意的人。

## 它能做什么

- **报价单**：逐项明细、人民币大写、定金/尾款自动勾稽，不再口头报价
- **简易服务合同**：9 条中国场景条款框架，锁定范围、交付、验收、修改次数
- **收款确认单**：每笔到账留痕，累计已收/未收一目了然
- **对账台账**：月底看清谁付了定金、谁还欠尾款
- **催款话术**：提醒/明确/严肃三档，得体不伤和气

> 边界：本 Skill 不开具税务发票（发票请走税务系统），合同模板不构成
> 法律意见，大额或复杂交易请咨询执业律师。

## 安装与使用

把本仓库文件夹放进你的 Agent 的 skills 目录（如 Claude Code 的
`~/.claude/skills/`、Codex/Cursor 等支持 SKILL.md 的工具），
然后直接对 Agent 说：「帮我做个报价单，菜单设计 800，店招 1200，
先收一半定金。」

零依赖小工具（可选，Python 3）：

```bash
python3 scripts/amount_check.py to-rmb-caps 3600
# 叁仟陆佰元整
python3 scripts/amount_check.py check --items 800,1200 --deposit-rate 0.5 --paid 1000
```

## 目录

- `SKILL.md` — Skill 本体（工作流程、条款框架、输出规范）
- `templates/` — 报价单 / 合同 / 收款确认 / 台账四种版式
- `scripts/amount_check.py` — 人民币大写 + 金额勾稽校验
- `examples/` — 完整输入→输出示例

## 许可证

MIT，见 `LICENSE`。工作流思路参考 alirezarezvani/claude-skills
（MIT）中的 contract-and-proposal-writer 与 invoice-generator 类
Skill，正文与模板为面向中国小微经营场景的原创重写。

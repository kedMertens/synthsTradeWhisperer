# Synthetix Trades Twitter Bot

The project is part of [Open DeFi Hackathon](https://gitcoin.co/issue/snxgrants/open-defi-hackathon/4/100025662)

Twitter bot checks from [Synthetix Exchanges](https://thegraph.com/explorer/subgraph/synthetixio-team/synthetix-exchanges?selected=playground)
with determined delay for trades and reports any trade which occurs over a certain thershold.

The report is done with help of text-generation algorithm, [gpt-neo-1.3B](https://github.com/EleutherAI/gpt-neo), to make tweets a bit funnier to follow,
introduction seeds are used to set a mood for new text at the end details of trade are provided.

Bot is deployed and can be found at https://twitter.com/SynthsWhisperer

Delay is set to 5 min and threshold 1000$

from graph_flow import build_graph

app = build_graph()

if __name__ == "__main__":
    print("🧠 LangGraph 记忆型问答助手启动！（输入 exit 退出）")

    state = {
        "input": "",
        "output": "",
        "next": "",
        "history": []
    }

    while True:
        user_input = input("你想问什么？→ ")
        if user_input.lower() == "exit":
            break

        state["input"] = user_input
        result = app.invoke(state)

        state["history"] = result["history"]
        print("AI助手：", result["output"])

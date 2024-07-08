from loguru import logger

def task_A():
    logger_a = logger.bind(task="A")
    logger_a.info("Starting task A")

    logger_a.success("End of task A")

def task_B():
    logger_b = logger.bind(task="B")
    logger_b.info("Starting task B")
    logger_b.success("End of task B")

#logger.add("file_A.log", filter=lambda record: record["extra"]["task"] == "A")
#logger.add("file_B.log", filter=lambda record: record["extra"]["task"] == "B")

task_A()
task_B()

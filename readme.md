<a id="readme-top"></a>
# Learning Progress Tracker


## About The Project
This is a command line app that tracks your course progress. It is designed to track the number of hours you have spent on a course and the number of hours you have left to complete the course.

<!-- Getting Started -->
## Getting Started
### Install LPT CLI
> Download the executable file and add it to your path.

### Start LPT CLI
```bash
> lpt
```
![CLI Welcome Snapshot](./images/lpt.png)

> This will start the LPT CLI and you will be prompted to enter commands.


<!-- Usage -->
## Usage
### Add Task
```bash
> add <task_name> <total_hours>
```
> This will add a task to the list of tasks. The task name must be unique. The total hours must be a positive integer.

### Show Task
```bash
> show <task_name> [Options]
```
> **Default**: Show task details
> 
> **Options**:
> - `-s` or `-short`: Show a short summary of the task


![CLI Snapshot](./images/add_and_show.png)

### List Tasks
```bash
> list [Options]
```
![CLI Snapshot](./images/list.png)
>**Default**: {active} {notcomplete} tasks

>**Options**:
>- `-all`: List all tasks
>- `-active`: List active tasks
>- `-inactive`: List inactive tasks
>- `-completed`: List completed tasks
>- `-notcomplete`: List incomplete tasks

### Edit Task
```bash
> edit <task_name> [Options]
```
![CLI Snapshot](./images/edit.png)
Options:
> a attribute value pair. The attribute must be one of the following:
> - `name`: The new name of the task
> - `total_time`: The new total hours of the task
> - `spent_time`: The number of hours spent on the task. Note that you can also use the `spent` command to add hours spent on a task.

### Spend Time on Task
```bash
> spent <task_name> <hours>
```
![CLI Snapshot](./images/spent.png)
>This will add the number of hours spent on a task. The hours must be a positive integer.


### Delete Task
```bash
> delete <task_name> [Options]
```
> **Default**: soft delete task. The task will be marked as inactive. (This is like archiving the task)
> 
> **Options**:
> - `-h` or `-hard`: hard delete task. The task will be permanently deleted.

### Restore Task
```bash
> restore <task_name>
```
> This will restore a task that has been deleted (soft deleted), making it active again.

![CLI Snapshot](./images/archive_and_restore.png)

### Clearing console
```bash
> clear
```
> This will clear the console.

### Help
```bash
> help
```
![CLI Snapshot](./images/help.png)

### exit
```bash
> exit
```
![CLI Snapshot](./images/exit.png)

> This will exit the LPT CLI.


<a href="#readme-top"><img width="50" height="50" src="https://img.icons8.com/ios-filled/50/circled-up-2.png" alt="circled-up-2" style="background-color: #ffffff; border-radius: 50%; display: inline-block; float: right; height: 50px; overflow: hidden; position: relative;" />
</a>
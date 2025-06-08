from task_tracker.cli import main
from task_tracker.models import init_db

if __name__ == '__main__':
    init_db()
    main()

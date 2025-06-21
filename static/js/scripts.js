// Main parent list where all tasks items are displayed
const taskList = document.getElementById('task-list');

// Toggle
taskList.addEventListener('click', (event) => {
  if (event.target.classList.contains('status-icon')) {
    // define constants for the status icon and task item
    const statusIcon = event.target;
    const taskItem = statusIcon.closest('.widget-task-item'); // Closest parent .widget-task-item

    // Toggle the 'checked' class on the status icon
    statusIcon.classList.toggle('checked');

    // If icon is checked, trigger slide out
    if (statusIcon.classList.contains('checked')) {
      if (taskItem) {
        taskItem.classList.add('slide-out');
        // Remove task item once animation ends
        taskItem.addEventListener(
          'transitionend',
          () => {
            taskItem.remove(); // remove from HTML
            // remove from db in future, and add it to completed tasks
          },
          { once: true }
        ); // Use {once: true} to ensure the event listener is removed after execution
      }
    }
  }
});

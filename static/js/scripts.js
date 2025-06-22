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

// ---- Tab Switching Logic ----

// Get all tab buttons
const taskFilterTabs = document.querySelectorAll('.tab-btn');

// Function to handle showing / hidiing tasks based on the active tab
function filterTasks(selectedStatus) {
  //  Get all task items
  const allTaskItems = document.querySelectorAll(
    '#task-list .widget-task-item'
  );

  // Loop through each task
  allTaskItems.forEach((taskItem) => {
    // Get status of current task item from its data-status attribute
    const taskStatus = taskItem.dataset.status;

    // Conditions to show/hide tasks based on selected status
    let shouldShow = false;
    if (selectedStatus === 'todo' && taskStatus === 'todo') {
      shouldShow = true; // Show if it's a todo task
    } else if (selectedStatus === 'completed' && taskStatus == 'completed') {
      shouldShow = true; // Show if it's a completed task
    } else if (selectedStatus === 'overdue' && taskStatus === 'overdue') {
      shouldShow = true; // Show if it's an overdue task
    }

    if (shouldShow) {
      taskItem.style.display = ''; // Default display (show the task)
    } else {
      taskItem.style.display = 'none'; // Hide the task
    }
  });
}

// Add click listeners for the tabs
taskFilterTabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    // Remove 'active' class from all tabs
    taskFilterTabs.forEach((t) => t.classList.remove('active'));
    // Add 'active' class to the clicked tab
    tab.classList.add('active');
    // Get the status from the clicked tab
    const selectedStatus = tab.dataset.status;
    // Call the filter function with the selected status
    filterTasks(selectedStatus);
  });
});

// Initial Filter / Default
filterTasks('todo'); // Show todo tasks by default

// ---- Task Expansion/Collapse Logic ----
taskList.addEventListener('click', (event) => {
  if (event.target.classList.contains('expand-icon')) {
    const expandIcon = event.target; // reference to the icon
    const parentTaskItem = expandIcon.closest('.widget-task-item.is-parent'); // find the closest parent task item

    if (parentTaskItem) {
      parentTaskItem.classList.toggle('expanded');
    }
  }
});

// ----- Modal Logic -----
const addTaskModal = document.getElementById('add-task-modal');
const fabAddTask = document.getElementById('fab-add-task');
const modalCloseBtn = addTaskModal.querySelector('.close-modal-btn');

// Open/Close modal function
function toggleModal() {
  addTaskModal.classList.toggle('active');
}

if (fabAddTask) {
  fabAddTask.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent default link behaviour
    toggleModal();
  });
}

if (modalCloseBtn) {
  modalCloseBtn.addEventListener('click', toggleModal);
}

// Close Modal when clicking outside the modal content or when escaping
if (addTaskModal) {
  addTaskModal.addEventListener('click', (event) => {
    if (event.target === addTaskModal) {
      toggleModal();
    }
  });
}

const generateTaskModal = document.getElementById('generate-task-modal');
const generateTaskButton = document.getElementById('open-generate-task-modal');
const generateModalCloseBtn = generateTaskModal.querySelector(
  '.close-modal-btn.generate-modal-close'
);

const generateFormStage = document.getElementById('generate-form-stage');
const generateLoadingStage = document.getElementById('generate-loading-stage');
const generatePreviewStage = document.getElementById('generate-preview-stage');

const generateButton = document.getElementById('generate-btn');
const confirmTaskButton = document.getElementById('confirm-task-btn');
const editTaskButton = document.getElementById('edit-task-btn');

function showGenerateModalStage(stageElement) {
  const stages = generateTaskModal.querySelectorAll('.modal-stage');
  stages.forEach((stage) => stage.classList.remove('active'));
  stageElement.classList.add('active');
}

function openGenerateTaskModal() {
  if (generateTaskModal) {
    generateTaskModal.classList.add('active');
    showGenerateModalStage(generateFormStage); // Show the form stage by default
  }
}

function closeGenerateTaskModal() {
  if (generateTaskModal) {
    generateTaskModal.classList.remove('active');
  }
}

if (generateTaskButton) {
  generateTaskButton.addEventListener('click', () => {
    openGenerateTaskModal();
  });
}

if (generateModalCloseBtn) {
  generateModalCloseBtn.addEventListener('click', closeGenerateTaskModal);
}

if (generateTaskModal) {
  generateTaskModal.addEventListener('click', (event) => {
    if (event.target === generateTaskModal) {
      closeGenerateTaskModal();
    }
  });
}

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    if (addTaskModal && addTaskModal.classList.contains('active')) {
      toggleModal();
    } else if (
      generateTaskModal &&
      generateTaskModal.classList.contains('active')
    ) {
      closeGenerateTaskModal();
    }
  }
});

if (generateButton) {
  generateButton.addEventListener('click', () => {
    const objective = document.getElementById('objective-input').value;
    const dueDate = document.getElementById('generate-task-deadline').value;
    const priority = document.getElementById('generate-task-priority').value;
    const scope = document.getElementById('generate-task-scope').value;

    console.log(
      `generating tasks with ${objective}, ${dueDate}, ${priority}, ${scope}`
    );

    showGenerateModalStage(generateLoadingStage);

    // Simulate API call
    setTimeout(() => {
      showGenerateModalStage(generatePreviewStage);
    }, 2000); // placeholder for generation time
  });
}

if (confirmTaskButton) {
  confirmTaskButton.addEventListener('click', () => {
    closeGenerateTaskModal();
  });
}

if (editTaskButton) {
  editTaskButton.addEventListener('click', () => {
    showGenerateModalStage(generateFormStage);
  });
}

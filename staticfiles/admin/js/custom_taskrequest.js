document.addEventListener("DOMContentLoaded", function () {
  const teamField = document.getElementById("id_preferred_team");
  const taskTypeField = document.getElementById("id_task_type");

  // Helper to clear task type options
  function clearTaskTypeOptions() {
    taskTypeField.innerHTML = "";
    const option = document.createElement("option");
    option.value = "";
    option.text = "Select a Task Type";
    taskTypeField.appendChild(option);
  }

  // Helper to fetch task types for the selected team
  function fetchTaskTypesForTeam(teamName) {
    fetch(`/api/task-types-for-team/${teamName}/`)
      .then(response => response.json())
      .then(data => {
        clearTaskTypeOptions();
        data.forEach(taskName => {
          const option = document.createElement("option");
          option.value = taskName;
          option.text = taskName;
          taskTypeField.appendChild(option);
        });
        taskTypeField.disabled = false;
      })
      .catch(error => {
        console.error("Error fetching task types:", error);
        clearTaskTypeOptions();
        taskTypeField.disabled = true;
      });
  }

  // Initial setup
  if (teamField && taskTypeField) {
    taskTypeField.disabled = true;

    teamField.addEventListener("change", function () {
      const selectedTeam = teamField.value;
      if (selectedTeam) {
        fetchTaskTypesForTeam(selectedTeam);
      } else {
        clearTaskTypeOptions();
        taskTypeField.disabled = true;
      }
    });
  }
});

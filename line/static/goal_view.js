document.addEventListener("DOMContentLoaded", (event) => {
    let cycleTime = document.getElementById("cycle-time");
    let startTimer = document.getElementById("start-timer");
    let stopTimer = document.getElementById("stop-timer");
    let currentGoalUnits = document.getElementById("current-goal-units");
    let actualUnits = document.getElementById("actual-units");
    let unitDone = document.getElementById("unit-done");
    let unitRemove = document.getElementById("unit-remove");
    let currentDate = document.getElementById("current-date");
    let actual = document.getElementById("actual");
    let real_time_goal = document.getElementById("real_time_goal");
    let submit = document.getElementById("submit");
    let actual_container = document.getElementById("actual-container");

    console.log(cycleTime.textContent);

    if (is_active === 'False'){
        startTimer.disabled = true;
        stopTimer.disabled = true;
        submit.disabled = true;
        unitDone.disabled = true;
        unitRemove.disabled = true;
    }

    function update_actual_color(){
        console.log(warning_units)
        console.log(error_units)
        console.log(actualUnits.textContent)
        console.log(currentGoalUnits.innerHTML)
        if ((currentGoalUnits.innerHTML - actualUnits.textContent) >= warning_units){
            actual_container.style.background = "yellow";
            console.log(currentGoalUnits.innerHTML - actualUnits.textContent)
        }
        if ((currentGoalUnits.innerHTML - actualUnits.textContent) >= error_units){
            actual_container.style.background = "red";
            console.log(currentGoalUnits.innerHTML - actualUnits.textContent)
        }
        if ((currentGoalUnits.innerHTML - actualUnits.textContent) < warning_units){
            actual_container.style.background = "transparent";
            console.log(currentGoalUnits.innerHTML - actualUnits.textContent)
        }

    }

    update_actual_color();

    function update_goal() {
        update_actual_color();
        $.ajax({
        headers: { "X-CSRFToken": token },
        data: {'actual_units' : actualUnits.textContent, 'goal_units' : currentGoalUnits.innerHTML, 'current_line' : current_line }, // get the form data
        url: "update_goal",
        dataType: 'json',
        method: "POST",
        // on success
        success: function (response) {
            if (response.test == true) {
                console.log('Success')
            }
            else {
                console.log('Failure')

            }

        },
        // on error
        error: function (response) {
            // alert the error if any error occured
            console.log(response.responseJSON.errors)
            }
        });
    }

    const startCycleTimer = () => {
        startTimer.disabled = true;
        let units = parseInt(currentGoalUnits.textContent);
        let originalCycleTime = parseInt(default_cycle_time);
        let currentTimer = parseInt(cycleTime.textContent);
        console.log(currentTimer);
        let countDown = setInterval(function(){
            console.log(currentTimer--);
            cycleTime.innerHTML = currentTimer;
            if (currentTimer === 0){
                currentTimer = originalCycleTime;
                units++;
                currentGoalUnits.innerHTML = units;
                real_time_goal.value = units;
                update_goal();
            }
        }, 1000);

        const stopCycleTimer = () => {
            startTimer.disabled = false;
            clearInterval(countDown)
        }

        stopTimer.onclick = stopCycleTimer;
    }

    const addUnit = () => {
        let unitTotal = parseInt(actualUnits.textContent);
        unitTotal++;
        actualUnits.innerHTML = unitTotal;
        actual.value = unitTotal;
        update_goal();
    };

    const removeUnit = () => {
        let unitTotal = parseInt(actualUnits.textContent);
        if (unitTotal === 0){
            actualUnits.innerHTML = 0;
        } else {
            unitTotal--;
            actualUnits.innerHTML = unitTotal;
        }
        update_goal();
        
    }

    startTimer.addEventListener("click", startCycleTimer);
    unitDone.addEventListener("click", addUnit);
    unitRemove.addEventListener("click", removeUnit);


    currentDate.innerHTML = 'Date <br>' + new Date().toLocaleDateString("en-US");


})
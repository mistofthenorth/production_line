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

    console.log(cycleTime.textContent);

    const startCycleTimer = () => {
        startTimer.classList.add("invisible");
        let units = parseInt(currentGoalUnits.textContent)
        let originalCycleTime = parseInt(cycleTime.textContent);
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
                console.log('We hit zero')
                $.ajax({
                    headers: { "X-CSRFToken": token },
                    data: {'thing' : actualUnits.textContent }, // get the form data
                    url: "console_print",
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
        }, 1000);

        const stopCycleTimer = () => {
            startTimer.classList.remove("invisible");
            clearInterval(countDown)
        }

        stopTimer.onclick = stopCycleTimer;
    }

    const addUnit = () => {
        let unitTotal = parseInt(actualUnits.textContent);
        unitTotal++;
        actualUnits.innerHTML = unitTotal;
        actual.value = unitTotal;
    };

    const removeUnit = () => {
        let unitTotal = parseInt(actualUnits.textContent);
        if (unitTotal === 0){
            actualUnits.innerHTML = 0;
        } else {
            unitTotal--;
            actualUnits.innerHTML = unitTotal;
        }
        
    }

    startTimer.addEventListener("click", startCycleTimer);
    unitDone.addEventListener("click", addUnit);
    unitRemove.addEventListener("click", removeUnit);


    currentDate.innerHTML = 'Date <br>' + new Date().toLocaleDateString("en-US");


})
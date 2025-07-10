// Define la función en el ámbito global
function updateProgressStepper(currentStep) {
    const steps = document.querySelectorAll('.progress-stepper .step');
    const lineSegments = document.querySelectorAll('.progress-stepper .line-segment');
    const totalSteps = steps.length;

    steps.forEach((step, index) => {
        const stepNumber = index + 1;
        if (stepNumber < currentStep) {
            step.classList.add('completed');
            step.classList.remove('active');
        } else if (stepNumber === currentStep) {
            step.classList.add('active');
            step.classList.remove('completed');
        } else {
            step.classList.remove('active');
            step.classList.remove('completed');
        }
    });

    lineSegments.forEach((line, index) => {
        const lineSegmentNumber = index + 1;
        if (lineSegmentNumber <= currentStep - 1) {
            line.style.width = 'calc(100% / ' + (totalSteps - 1) + ')';
        } else {
            line.style.width = '0%';
        }
    });
}

// Exponer globalmente
window.updateProgressStepper = updateProgressStepper;

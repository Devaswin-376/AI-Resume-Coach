async function analyzeResume() {
    const fileInput = document.getElementById('resumeFile');
    const file = fileInput.files[0];

    if (!file){
        alert ("Please select a file to upload.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try{
        const response = await fetch('http://localhost:8000/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            document.getElementById("result").innerHTML =
            `<p>${data.error}</p>`;
            return;
        }

        document.getElementById("result").innerHTML = `
            <h2>Resume Score: ${data.analysis.resume_score}</h2>

            <h3>Candidate Summary</h3>
            <p>${data.analysis.candidate_summary}</p>

            <h3>Technical Skills</h3>
            <ul>
                ${data.analysis.technical_skills.map(skill =>
                    `<li>${skill}</li>`
                ).join("")}
            </ul>

            <h3>Recommended Job Roles</h3>
            <ul>
                ${data.analysis.job_roles.map(role =>
                    `<li>${role}</li>`
                ).join("")}
            </ul>

            <h3>Skill Gaps</h3>
            <ul>
                ${data.analysis.skill_gaps.map(gap =>
                    `<li>${gap}</li>`
                ).join("")}
            </ul>
            <h3>Recommended projects</h3>
            <ul>
                ${data.analysis.recommended_projects.map(project => 
                    `<li>${project}</li>`
                ).join("")}
            </ul>
        `;

    }
    catch (error) {
        document.getElementById('result').innerHTML = `
        <p style="color: red;">Error analyzing resume: ${error.message}</p>
        `;
    }
}
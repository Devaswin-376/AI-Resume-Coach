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
        const response = await fetch('https://ai-resume-coach-tau.vercel.app/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.analysis.error) {
            document.getElementById('result').innerHTML = data.analysis.error;
            return;
        }

        document.getElementById("result").innerHTML = `
            <div class="score-card">
                <h2>Resume Score: ${data.analysis.resume_score}</h2>
            </div>

            <div class="section">
                <h3>Candidate Summary</h3>
                <p>${data.analysis.candidate_summary}</p>
            </div>

            <div class="section">
                <h3>Technical Skills</h3>
                <ul>
                    ${data.analysis.technical_skills.map(skill =>
                        `<li>${skill}</li>`
                    ).join("")}
                </ul>
            </div>

            <div class="section">
                <h3>Recommended Job Roles</h3>
                <ul>
                    ${data.analysis.job_roles.map(role =>
                        `<li>${role}</li>`
                    ).join("")}
                </ul>
            </div>

            <div class="section">
                <h3>Skill Gaps</h3>
                <ul>
                    ${data.analysis.skill_gaps.map(gap =>
                        `<li>${gap}</li>`
                    ).join("")}
                </ul>
            </div>

            <div class="section">
                <h3>Recommended projects</h3>
                <ul>
                    ${data.analysis.recommended_projects.map(project => 
                    `<li>${project}</li>`
                ).join("")}
                </ul>
            </div>
        `;

    }
    catch (error) {
        document.getElementById('result').innerHTML = `
        <p style="color: red;">Error analyzing resume: ${error.message}</p>
        `;
    }
}
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const errorsContainer = document.createElement("ul");
    errorsContainer.style.color = "red";
    form.prepend(errorsContainer);

    form.addEventListener("submit", (event) => {
        errorsContainer.innerHTML = "";

        const errors = [];

        const fieldsToValidate = {
            nom: "Nom",
            espece: "Espèce",
            race: "Race",
            description: "Description",
            courriel: "Courriel",
            adresse: "Adresse",
            ville: "Ville",
            cp: "Code postal"
        };

        const containsComma = (value) => value.includes(',');

        for (const [fieldName, fieldLabel] of Object.entries(fieldsToValidate)) {
            const fieldValue = form[fieldName].value.trim();
            if (containsComma(fieldValue)) {
                errors.push(`Le champ '${fieldLabel}' ne peut pas contenir de virgule.`);
            }
        }

        const nom = form.nom.value.trim();
        const age = form.age.value.trim();
        const courriel = form.courriel.value.trim();
        const cp = form.cp.value.trim();

        if (nom.length < 3 || nom.length > 20) {
            errors.push("Le nom de l'animal doit comporter entre 3 et 20 caractères.");
        }

        if (!/^\d+$/.test(age) || age < 0 || age > 30) {
            errors.push("L'âge doit être un nombre entre 0 et 30.");
        }

        if (!/^\S+@\S+\.\S+$/.test(courriel)) {
            errors.push("L'adresse courriel n'est pas valide.");
        }

        if (!/^[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d$/.test(cp)) {
            errors.push("Le code postal doit être au format canadien (ex. H3Z 2Y7).");
        }

        if (errors.length > 0) {
            event.preventDefault();
            errors.forEach((error) => {
                const li = document.createElement("li");
                li.textContent = error;
                errorsContainer.appendChild(li);
            });
        }
    });
});

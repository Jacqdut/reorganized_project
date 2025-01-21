const fs = require('fs');
const path = require('path');
const eslint = require('eslint');

// Initialize ESLint
const cli = new eslint.CLIEngine({
  fix: true,
  extensions: ['.js', '.jsx', '.ts', '.tsx'],
  useEslintrc: true,
});

const directoryPath = path.join(__dirname, 'src'); // Your source code directory

// Helper function to remove unused variables and imports
function removeUnusedVarsAndImports() {
  fs.readdir(directoryPath, (err, files) => {
    if (err) {
      console.log('Error reading directory:', err);
      return;
    }

    files.forEach((file) => {
      const filePath = path.join(directoryPath, file);
      const fileExtension = path.extname(file);

      // Only process JavaScript and JSX files
      if (fileExtension === '.js' || fileExtension === '.jsx') {
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const lintResults = cli.executeOnText(fileContent, filePath);
        
        // Check if there are linting errors and apply fixes
        if (lintResults.errorCount === 0) {
          const fixedContent = lintResults.results[0].output;
          fs.writeFileSync(filePath, fixedContent, 'utf-8');
          console.log(`Cleaned up file: ${filePath}`);
        }
      }
    });
  });
}

removeUnusedVarsAndImports();

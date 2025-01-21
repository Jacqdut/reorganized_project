// remove-unused-vars.js

const { API, FileInfo } = require('jscodeshift');

// Function to remove unused imports
function removeUnusedImports(root) {
  root.find(j.ImportDeclaration)
    .forEach(path => {
      const specifiers = path.node.specifiers;
      const unusedSpecifiers = specifiers.filter(specifier => {
        return !specifier.local || !path.scope.lookup(specifier.local.name);
      });

      unusedSpecifiers.forEach(specifier => {
        path.node.specifiers = path.node.specifiers.filter(s => s !== specifier);
      });

      // If no specifiers remain, remove the import declaration entirely
      if (path.node.specifiers.length === 0) {
        path.prune();
      }
    });
}

// Function to remove unused variables
function removeUnusedVariables(root) {
  root.find(j.VariableDeclarator)
    .forEach(path => {
      const variable = path.node.id.name;
      const references = path.scope.lookup(variable) ? path.scope.lookup(variable).references : [];
      if (references.length === 0) {
        path.prune();
      }
    });
}

// Main function that applies transformations
module.exports = function (fileInfo, api) {
  const j = api.jscodeshift;
  const root = j(fileInfo.source);

  // Run the transformations
  removeUnusedImports(root);
  removeUnusedVariables(root);

  return root.toSource({ quote: 'single' });
};

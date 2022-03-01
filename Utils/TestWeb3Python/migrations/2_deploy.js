const pProcess = artifacts.require("PrintingProcess");

module.exports = function (deployer) {
  deployer.deploy(pProcess);
};

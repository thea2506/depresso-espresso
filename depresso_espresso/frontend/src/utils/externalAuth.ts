const getExternalNode = (externalUrl: string) => {
  if (
    externalUrl.includes(
      "https://deadly-bird-justin-ce5a27ea0b51.herokuapp.com"
    )
  ) {
    return {
      host: externalUrl,
      username: "thedeadlybird",
      password: "2p(F6x@9?Y5D\x07<z0CF",
    };
  } else if (
    externalUrl.includes("https://web-wizards-roop-06e9f4b1fec9.herokuapp.com")
  ) {
    return {
      host: externalUrl,
      username: "wizards",
      password: "0@UR0db$Rw84",
    };
  } else {
    return {
      host: externalUrl,
      username: "",
      password: "",
    };
  }
};

export { getExternalNode };

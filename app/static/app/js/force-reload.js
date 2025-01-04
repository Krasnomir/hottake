// sometimes when user uses browser back button the votes dont get updated which may result in vote counters being all messed up like upvote counter showing a negative number
// note that it doesnt actually affect the vote count server-side
// following code makes sure that the page is reloded so that the user won't see the old cached result

window.addEventListener( "pageshow", (event) => {
    const historyTraversal = event.persisted || ( typeof window.performance != "undefined" && window.performance.navigation.type === 2 );
    if (historyTraversal) window.location.reload();
});
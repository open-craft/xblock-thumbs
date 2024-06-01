// @ts-check
import {
    html,
    useFields,
    useCallback,
    registerPreactXBlock,
    callHandler,
} from 'xblock2-client-v0';

function ThumbsBlock(props) {
    const {
        upvotes,
        downvotes,
    } = useFields(props);

    const upvote = useCallback(() => {
        callHandler(props.usageKey, "vote", { voteType: "up" });
    }, []);

    const downvote = useCallback(() => {
        callHandler(props.usageKey, "vote", { voteType: "down" });
    }, []);

    return html`
        <p>
            <span class="upvote" onClick=${upvote}><span class="count">${upvotes}</span>↑</span>
            <span class="downvote" onClick=${downvote}><span class="count">${downvotes}</span>↓</span>
        </p>
        <style>
        .upvote, .downvote {
            cursor: pointer;
            border: 1px solid #888;
            padding: 0 .5em;
        }
        .upvote { color: green; }
        .downvote { color: red; }
        </style>
    `;
}

registerPreactXBlock(ThumbsBlock, 'thumbs', {shadow: true});

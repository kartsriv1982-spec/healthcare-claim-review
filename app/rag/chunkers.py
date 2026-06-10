from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    TokenTextSplitter
)


def fixed_chunking(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)


def token_chunking(documents):

    splitter = TokenTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_documents(documents)


def parent_child_chunking(documents):

    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200
    )

    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    parents = parent_splitter.split_documents(documents)

    result = []

    for parent_id, parent in enumerate(parents):

        children = child_splitter.create_documents(
            [parent.page_content]
        )

        for child in children:

            child.metadata.update({
                "parent_id": parent_id,
                "chunk_type": "child"
            })

            result.append(child)

    return result


def section_chunking(documents):

    text = "\n".join(
        d.page_content for d in documents
    )

    sections = text.split("SECTION")

    result = []

    for idx, section in enumerate(sections):

        if not section.strip():
            continue

        result.append(
            Document(
                page_content=f"SECTION {section}",
                metadata={
                    "section_id": idx,
                    "chunk_type": "section"
                }
            )
        )

    return result


CHUNKING_STRATEGIES = {
    "fixed": fixed_chunking,
    "token": token_chunking,
    "parent_child": parent_child_chunking,
    "section": section_chunking
}
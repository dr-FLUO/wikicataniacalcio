with open("quartz/styles/custom.scss", "r", encoding="utf-8") as f:
    text = f.read()

old_block = """.nfc-masthead__actions {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.45rem 0.85rem;
  border-right: 1px solid var(--wiki-border-hairline);
}"""

new_block = """.nfc-masthead__actions {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-end;
  gap: 0.25rem;
  padding: 0.35rem 0.85rem;
  border-right: 1px solid var(--wiki-border-hairline);
}

.nfc-update-meta {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-family: var(--font-mono, monospace);
  font-size: 0.68rem;
  font-weight: 600;
  color: #10b981;
  letter-spacing: 0.02em;
  white-space: nowrap;

  &__dot {
    width: 6px;
    height: 6px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
    animation: cataniaPulse 2s infinite;
  }

  &__text {
    line-height: 1;
  }
}

:root[saved-theme="dark"] .nfc-update-meta {
  color: #34d399;
}"""

if old_block in text:
    text = text.replace(old_block, new_block, 1)
    with open("quartz/styles/custom.scss", "w", encoding="utf-8", newline="\r\n") as f:
        f.write(text)
    print("SUCCESS: custom.scss updated")
else:
    print("WARNING: old_block not found")

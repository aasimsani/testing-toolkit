/** Fetch the fields that the profile widget shows for one user. */
export async function getProfile(baseUrl, userId) {
  const res = await fetch(`${baseUrl}/users/${userId}`, { headers: { Accept: 'application/json' } });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`users-api responded ${res.status}`);
  const body = await res.json();
  return {
    name: body.displayName,
    avatarUrl: body.avatarUrl,
    badge: body.plan === 'pro' ? 'PRO' : null,
  };
}

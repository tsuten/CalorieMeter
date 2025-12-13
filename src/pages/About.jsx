import '../styles/pageStyle.css'
import { Paper, Title, Text, Stack, Group, Badge, Divider, Table, Anchor } from '@mantine/core'
import {
  appDescription,
  about,
  credits,
  contactInfo,
} from '../dummy-data/about.js'

function About() {
  return (
    <div className="page-container">
      <h1 className="page-title">About</h1>
      <div className="page-content">
        <Stack gap="lg">
          {/* アプリケーション概要 */}
          {/* <Paper p="md" radius="md" withBorder>
            <Title order={2} mb="md">{appDescription.title}</Title>
            {appDescription.description.map((text, index) => (
              <Text key={index} size="md" mb={index === 0 ? 'sm' : undefined}>
                {text}
              </Text>
            ))}
          </Paper> */}

          {/* バージョン情報 */}
          <Paper p="md" radius="md" withBorder>
            <Title order={2} mb="md">About</Title>
            <Stack gap="xs">
              <Group justify="space-between">
                <Text size="md" fw={500}>アプリケーション名</Text>
                <Text size="md">{about.appName}</Text>
              </Group>
              <Divider />
              <Group justify="space-between">
                <Text size="md" fw={500}>バージョン</Text>
                <Text size="md" color="gray">{about.version}</Text>
              </Group>
              <Divider />
              <Group justify="space-between">
                <Text size="md" fw={500}>リポジトリ</Text>
                <Text size="md">{about.repository}</Text>
              </Group>
            </Stack>
          </Paper>

          {/* クレジット */}
          <Paper p="md" radius="md" withBorder>
            <Title order={2} mb="md">クレジット</Title>
            <Table striped highlightOnHover withColumnBorders>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>ライブラリ名</Table.Th>
                  <Table.Th>用途</Table.Th>
                  <Table.Th>リンク</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {credits.map((credit, index) => (
                  <Table.Tr key={index}>
                    <Table.Td>{credit.name}</Table.Td>
                    <Table.Td>{credit.usage}</Table.Td>
                    <Table.Td>
                      <Anchor href={credit.link} target="_blank" rel="noopener noreferrer">
                        {credit.link}
                      </Anchor>
                    </Table.Td>
                  </Table.Tr>
                ))}
              </Table.Tbody>
            </Table>
          </Paper>

          {/* お問い合わせ */}
          {/* <Paper p="md" radius="md" withBorder>
            <Title order={2} mb="md">{contactInfo.title}</Title>
            <Text size="md" c="dimmed">
              {contactInfo.description}
            </Text>
          </Paper> */}
        </Stack>
      </div>
    </div>
  )
}

export default About

